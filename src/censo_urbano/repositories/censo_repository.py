from pathlib import Path

import pandas as pd

from src.censo_urbano.config import CD_MUN_MARINGA

# Formato oficial dos Agregados por Setor Censitário (Censo 2022, confirmado em 2026-07-16):
# separador ";", decimal ",", encoding ISO-8859-1 (latin1), "X" = sigilo estatístico (ausente).
_READ_CSV_KWARGS = {"sep": ";", "decimal": ",", "encoding": "latin1", "na_values": ["X"]}


def _ler_csv_censo(caminho: Path, coluna_setor: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, dtype={coluna_setor: str}, **_READ_CSV_KWARGS)
    return df.rename(columns={coluna_setor: "CD_SETOR"})


def ler_basico(caminho: Path, cd_mun: str = CD_MUN_MARINGA) -> pd.DataFrame:
    """Universo completo de setores do município (inclui setores sem domicílios)."""
    df = _ler_csv_censo(caminho, "CD_SETOR")
    df["CD_MUN"] = df["CD_MUN"].astype(str)
    return df[df["CD_MUN"] == cd_mun].reset_index(drop=True)


def ler_domicilio1(caminho: Path) -> pd.DataFrame:
    """Características do domicílio, parte 1 (V00001-089, inclui espécie do domicílio)."""
    return _ler_csv_censo(caminho, "CD_setor")


def ler_domicilio2(caminho: Path) -> pd.DataFrame:
    """Características do domicílio, parte 2 (V00090-495, inclui água/esgoto/lixo/banheiro)."""
    return _ler_csv_censo(caminho, "setor")


def ler_domicilio3(caminho: Path) -> pd.DataFrame:
    """Características do domicílio, parte 3 (V00496-643, inclui moradores por faixa de banheiro)."""
    return _ler_csv_censo(caminho, "setor")


def carregar_setores(
    basico_path: Path,
    domicilio1_path: Path,
    domicilio2_path: Path,
    domicilio3_path: Path,
    cd_mun: str = CD_MUN_MARINGA,
) -> pd.DataFrame:
    """Junta as 4 tabelas por CD_SETOR, um setor por linha.

    Left join a partir de `basico` (universo completo de setores do município):
    setores sem domicílios não aparecem nos arquivos de características e viram
    NaN aqui — é o caso `sem_dado` tratado no domínio (domain/index.py).
    """
    resultado = ler_basico(basico_path, cd_mun=cd_mun)
    for caminho, leitor in (
        (domicilio1_path, ler_domicilio1),
        (domicilio2_path, ler_domicilio2),
        (domicilio3_path, ler_domicilio3),
    ):
        dom = leitor(caminho)
        resultado = resultado.merge(dom, on="CD_SETOR", how="left")
    return resultado
