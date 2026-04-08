import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "maringa_smartcity_lotes.xlsx"


def normalizar(df: pd.DataFrame, coluna: str) -> pd.Series:
    min_val = df[coluna].min()
    max_val = df[coluna].max()

    if max_val == min_val:
        return pd.Series([0] * len(df))

    return (df[coluna] - min_val) / (max_val - min_val)


def load_maringa_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH)

    # remove colunas completamente vazias
    df = df.dropna(axis=1, how='all')

    # limpa nomes
    df.columns = df.columns.str.strip()

    # Normalizações
    colunas_norm = [
        "Inst_Saude", "Inst_Educacao", "Transporte_Publico",
        "Espacos_Publicos", "Inst_Culturais", "Inst_Esportivas",
        "Lotes_Vagos", "Densidade_Habitacional",
        "Intensidade_Ocupacao", "Valor_m2"
    ]

    for col in colunas_norm:
        df[f"{col}_norm"] = normalizar(df, col)

    # Índice de Infraestrutura Urbana (IIU)
    df["IIU"] = (
        df["Inst_Saude_norm"] +
        df["Inst_Educacao_norm"] +
        df["Transporte_Publico_norm"]
    ) / 3

    # Índice de Qualidade Urbana (IQU)
    df["IQU"] = (
        df["Espacos_Publicos_norm"] +
        df["Inst_Culturais_norm"] +
        df["Inst_Esportivas_norm"] +
        df["IIU"]
    ) / 4

    # Índice de Ocupação do Solo (IOS)
    df["IOS"] = (
        df["Densidade_Construida"] +
        df["Intensidade_Ocupacao_norm"]
    ) / 2

    # Índice de Ociosidade Urbana (IOU)
    df["IOU"] = df["Lotes_Vagos_norm"]

    # Índice de Adensamento Inteligente (IAI)
    df["IAI"] = df["Densidade_Habitacional_norm"] * df["IOS"]

    # Índice de Valorização Urbana (IVU)
    df["IVU"] = df["Valor_m2_norm"]

    # Score final
    df["SCORE"] = (
        0.25 * df["IQU"] +
        0.25 * df["IIU"] +
        0.20 * df["IAI"] +
        0.15 * df["IVU"] -
        0.15 * df["IOU"]
    )

    return df
