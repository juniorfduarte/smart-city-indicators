import numpy as np
import pandas as pd
import pytest

from src.censo_urbano.services.iua_service import calcular_iua_setores

# Colunas mínimas necessárias para exercitar o pipeline completo, nos nomes
# reais do Censo 2022 (ver src/censo_urbano/config.py).
_COLUNAS_AGUA_TOTAL = [f"V00{n}" for n in range(111, 119)]  # V00111..V00118


def _setor(
    cd_setor: str,
    *,
    v0007: float,
    agua_adequada: float,
    agua_outras: float,
    esgoto_adequado: float,
    lixo_coletado: float,
    lixo_cacamba: float,
    especie_adequada: float,
    especie_outras: float,
    banheiro_1_domicilios: float,
    banheiro_1_moradores: float,
    cd_fcu: str = ".",  # "." = não está em aglomerado subnormal (caso real de Maringá)
) -> dict:
    linha = {"CD_SETOR": cd_setor, "v0007": v0007, "CD_FCU": cd_fcu}
    linha["V00111"] = agua_adequada
    for col in _COLUNAS_AGUA_TOTAL[1:]:
        linha[col] = 0.0
    linha[_COLUNAS_AGUA_TOTAL[-1]] = agua_outras
    linha["V00309"] = esgoto_adequado
    linha["V00397"] = lixo_coletado
    linha["V00398"] = lixo_cacamba
    linha["V00047"] = especie_adequada / 3
    linha["V00048"] = especie_adequada / 3
    linha["V00049"] = especie_adequada / 3
    linha["V00050"] = especie_outras
    linha["V00051"] = 0.0
    linha["V00052"] = 0.0
    linha["V00232"] = banheiro_1_domicilios
    linha["V00552"] = banheiro_1_moradores
    for col in ["V00233", "V00234", "V00235", "V00236", "V00237", "V00238"]:
        linha[col] = 0.0
    for col in ["V00553", "V00554", "V00555", "V00556", "V00557", "V00558"]:
        linha[col] = 0.0
    return linha


@pytest.fixture
def df_dois_setores():
    # Setor 111: melhores condições em todos os indicadores.
    # Setor 222: piores condições em todos os indicadores (dá variação p/ normalizar()).
    return pd.DataFrame([
        _setor(
            "111",
            v0007=100,
            agua_adequada=90,
            agua_outras=10,
            esgoto_adequado=70,
            lixo_coletado=60,
            lixo_cacamba=20,
            especie_adequada=95,
            especie_outras=5,
            banheiro_1_domicilios=100,
            banheiro_1_moradores=200,  # densidade 2 <= 4 -> adequado
        ),
        _setor(
            "222",
            v0007=50,
            agua_adequada=25,
            agua_outras=25,
            esgoto_adequado=10,
            lixo_coletado=5,
            lixo_cacamba=5,
            especie_adequada=30,
            especie_outras=20,
            banheiro_1_domicilios=50,
            banheiro_1_moradores=250,  # densidade 5 > 4 -> inadequado
        ),
    ])


class TestCalcularIuaSetores:
    def test_setor_sem_domicilios_e_sem_dado(self):
        df = pd.DataFrame([
            _setor(
                "333",
                v0007=0,
                agua_adequada=np.nan,
                agua_outras=np.nan,
                esgoto_adequado=np.nan,
                lixo_coletado=np.nan,
                lixo_cacamba=np.nan,
                especie_adequada=np.nan,
                especie_outras=np.nan,
                banheiro_1_domicilios=np.nan,
                banheiro_1_moradores=np.nan,
            ),
        ])
        resultado = calcular_iua_setores(df)
        linha = resultado.iloc[0]
        assert linha["sem_dado"]
        assert pd.isna(linha["d3"])
        assert pd.isna(linha["d4"])
        assert pd.isna(linha["iua"])

    def test_setor_com_menos_de_cinco_domicilios_e_sem_dado_mesmo_sem_supressao(self, df_dois_setores):
        # v0007=3 (< 5 => sem_dado pelo limiar oficial do IBGE), mas com variáveis
        # preenchidas normalmente — prova que a máscara explícita de sem_dado
        # funciona mesmo quando os indicadores dariam um número real (esgoto,
        # lixo e densidade de banheiro usam total_domicilios > 0 como
        # denominador, então não ficariam NaN sozinhos via propagação).
        df = pd.concat(
            [
                df_dois_setores,
                pd.DataFrame([
                    _setor(
                        "444",
                        v0007=3,
                        agua_adequada=2,
                        agua_outras=1,
                        esgoto_adequado=2,
                        lixo_coletado=1,
                        lixo_cacamba=1,
                        especie_adequada=2,
                        especie_outras=1,
                        banheiro_1_domicilios=3,
                        banheiro_1_moradores=6,  # densidade 2 <= 4 -> adequado
                    ),
                ]),
            ],
            ignore_index=True,
        )
        resultado = calcular_iua_setores(df)
        linha_444 = resultado[resultado["CD_SETOR"] == "444"].iloc[0]
        assert linha_444["sem_dado"]
        assert pd.isna(linha_444["d3"])
        assert pd.isna(linha_444["d4"])
        assert pd.isna(linha_444["iua"])

    def test_setor_com_melhores_condicoes_tem_iua_maximo(self, df_dois_setores):
        resultado = calcular_iua_setores(df_dois_setores)
        linha_111 = resultado[resultado["CD_SETOR"] == "111"].iloc[0]
        assert linha_111["d4"] == pytest.approx(1.0)
        assert linha_111["d3"] == pytest.approx(1.0)
        assert linha_111["iua"] == pytest.approx(1.0)

    def test_setor_com_piores_condicoes_tem_iua_proximo_do_minimo(self, df_dois_setores):
        resultado = calcular_iua_setores(df_dois_setores)
        linha_222 = resultado[resultado["CD_SETOR"] == "222"].iloc[0]
        assert linha_222["d4"] == pytest.approx(0.0)
        # D3 não chega a 0 pois "não aglomerado subnormal" é 1.0 para os dois setores.
        assert linha_222["d3"] == pytest.approx(1 / 3)
        assert linha_222["iua"] == pytest.approx(1 / 6)

    def test_setor_em_aglomerado_subnormal_reduz_d3(self, df_dois_setores):
        df = df_dois_setores.copy()
        df.loc[df["CD_SETOR"] == "111", "CD_FCU"] = "AB01"
        resultado = calcular_iua_setores(df)
        linha_111 = resultado[resultado["CD_SETOR"] == "111"].iloc[0]
        assert linha_111["d3"] == pytest.approx(2 / 3)

    def test_celula_suprimida_em_variavel_de_soma_equivale_a_zero_explicito(self, df_dois_setores):
        df_com_x = df_dois_setores.copy()
        df_com_x.loc[df_com_x["CD_SETOR"] == "111", "V00118"] = np.nan

        df_com_zero = df_dois_setores.copy()
        df_com_zero.loc[df_com_zero["CD_SETOR"] == "111", "V00118"] = 0.0

        resultado_x = calcular_iua_setores(df_com_x)
        resultado_zero = calcular_iua_setores(df_com_zero)

        pd.testing.assert_series_equal(resultado_x["d4"], resultado_zero["d4"])
        pd.testing.assert_series_equal(resultado_x["iua"], resultado_zero["iua"])
