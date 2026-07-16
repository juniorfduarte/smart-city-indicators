import pandas as pd

from src.censo_urbano.config import (
    AGUA_ADEQUADA_V00XXX,
    AGUA_TOTAL_V00XXX,
    ESGOTO_ADEQUADO_V00XXX,
    ESPECIE_ADEQUADA_V00XXX,
    ESPECIE_TOTAL_V00XXX,
    FAIXAS_BANHEIRO,
    LIXO_ADEQUADO_V00XXX,
    TOTAL_DOMICILIOS_V0007,
)
from src.censo_urbano.domain.dimensions import calcular_d3, calcular_d4
from src.censo_urbano.domain.index import calcular_iua, calcular_sem_dado
from src.censo_urbano.domain.indicators import (
    FaixaBanheiro,
    prop_agua,
    prop_densidade_banheiro,
    prop_especie_adequada,
    prop_esgoto,
    prop_lixo,
)
from src.censo_urbano.domain.normalization import normalizar


def _soma_variaveis(df: pd.DataFrame, colunas: list[str]) -> pd.Series:
    """Soma variáveis do Censo tratando célula suprimida ('X' -> NaN) como 0.

    Decisão de 2026-07-16 (ver CLAUDE.md): desvio consciente do spec original
    para indicadores que somam múltiplas variáveis (água, espécie, lixo).
    """
    return df[colunas].fillna(0).sum(axis=1)


def _montar_faixas_banheiro(df: pd.DataFrame) -> list[FaixaBanheiro]:
    return [
        FaixaBanheiro(
            nome=faixa["nome"],
            domicilios=df[faixa["domicilios_v00xxx"]].fillna(0),
            moradores=df[faixa["moradores_v00xxx"]].fillna(0),
            num_banheiros=faixa["num_banheiros"],
        )
        for faixa in FAIXAS_BANHEIRO
    ]


def _calcular_ind_nao_aglomerado_subnormal(df_setores: pd.DataFrame) -> pd.Series:
    """1.0 quando o setor não está em aglomerado subnormal (CD_FCU vazio/'.'), 0.0 caso contrário.

    Indicador binário do IBEU original — não passa por normalizar() (não é uma
    proporção contínua). CD_FCU vem do arquivo básico (já presente em
    df_setores via censo_repository.carregar_setores). Em Maringá, CD_FCU é
    '.' para todos os setores (spec §6.2): não há aglomerado subnormal
    delimitado pelo IBGE na cidade.
    """
    cd_fcu = df_setores["CD_FCU"]
    return (cd_fcu.isna() | cd_fcu.isin([".", ""])).astype(float)


def calcular_iua_setores(df_setores: pd.DataFrame) -> pd.DataFrame:
    """Calcula sem_dado, D3, D4 e IUA para cada setor.

    df_setores: saída de `censo_repository.carregar_setores` (um setor por
    linha, já inclui CD_FCU do arquivo básico).
    """
    total_domicilios = df_setores[TOTAL_DOMICILIOS_V0007].astype(float)
    sem_dado = calcular_sem_dado(total_domicilios)

    agua_adequada = _soma_variaveis(df_setores, AGUA_ADEQUADA_V00XXX)
    agua_total = _soma_variaveis(df_setores, AGUA_TOTAL_V00XXX)
    ind_agua = normalizar(prop_agua(agua_adequada, agua_total))

    esgoto_adequado = _soma_variaveis(df_setores, ESGOTO_ADEQUADO_V00XXX)
    ind_esgoto = normalizar(prop_esgoto(esgoto_adequado, total_domicilios))

    lixo_adequado = _soma_variaveis(df_setores, LIXO_ADEQUADO_V00XXX)
    ind_lixo = normalizar(prop_lixo(lixo_adequado, total_domicilios))

    especie_adequada = _soma_variaveis(df_setores, ESPECIE_ADEQUADA_V00XXX)
    especie_total = _soma_variaveis(df_setores, ESPECIE_TOTAL_V00XXX)
    ind_especie_adequada = normalizar(prop_especie_adequada(especie_adequada, especie_total))

    faixas = _montar_faixas_banheiro(df_setores)
    ind_densidade_banheiro = normalizar(prop_densidade_banheiro(faixas, total_domicilios))

    ind_nao_aglomerado_subnormal = _calcular_ind_nao_aglomerado_subnormal(df_setores)

    d4 = calcular_d4(ind_agua, ind_esgoto, ind_lixo)
    d3 = calcular_d3(ind_nao_aglomerado_subnormal, ind_densidade_banheiro, ind_especie_adequada)
    iua = calcular_iua(d3, d4)

    # Máscara explícita: esgoto/lixo/densidade de banheiro usam total_domicilios
    # (externo, do básico) como denominador, não um total somado internamente
    # como água/espécie — por isso não ficam NaN sozinhos quando sem_dado=True
    # (poucos domicílios, mas total_domicilios ainda > 0).
    d3 = d3.where(~sem_dado)
    d4 = d4.where(~sem_dado)
    iua = iua.where(~sem_dado)

    return pd.DataFrame({
        "CD_SETOR": df_setores["CD_SETOR"],
        "sem_dado": sem_dado,
        "d3": d3,
        "d4": d4,
        "iua": iua,
    })
