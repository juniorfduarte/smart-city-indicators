import pandas as pd
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "maringa_smartcity_lotes.xlsx"


def normalizar(df: pd.DataFrame, coluna: str) -> pd.Series:
    min_val = df[coluna].min()
    max_val = df[coluna].max()

    if max_val == min_val:
        return pd.Series([0] * len(df))

    return (df[coluna] - min_val) / (max_val - min_val)


def to_snake_case(col: str) -> str:
    col = col.strip().lower()
    col = col.replace(" ", "_")
    col = re.sub(r"[^\w_]", "", col)
    return col


def load_maringa_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH)

    # limpeza
    df = df.dropna(axis=1, how='all')
    df.columns = [to_snake_case(col) for col in df.columns]

    # Normalizações
    colunas_norm = [
        "inst_saude", "inst_educacao", "transporte_publico",
        "espacos_publicos", "inst_culturais", "inst_esportivas",
        "lotes_vagos", "densidade_habitacional",
        "intensidade_ocupacao", "valor_m2"
    ]

    for col in colunas_norm:
        df[f"{col}_norm"] = normalizar(df, col)

    # Índices

    df["indice_infraestrutura_urbana"] = (
        df["inst_saude_norm"] +
        df["inst_educacao_norm"] +
        df["transporte_publico_norm"]
    ) / 3

    df["indice_qualidade_urbana"] = (
        df["espacos_publicos_norm"] +
        df["inst_culturais_norm"] +
        df["inst_esportivas_norm"] +
        df["indice_infraestrutura_urbana"]
    ) / 4

    df["indice_ocupacao_solo"] = (
        df["densidade_construida"] +
        df["intensidade_ocupacao_norm"]
    ) / 2

    df["indice_ociosidade_urbana"] = df["lotes_vagos_norm"]

    df["indice_adensamento_inteligente"] = (
        df["densidade_habitacional_norm"] *
        df["indice_ocupacao_solo"]
    )

    df["indice_valorizacao_urbana"] = df["valor_m2_norm"]

    df["smart_city_score"] = (
        0.25 * df["indice_qualidade_urbana"] +
        0.25 * df["indice_infraestrutura_urbana"] +
        0.20 * df["indice_adensamento_inteligente"] +
        0.15 * df["indice_valorizacao_urbana"] -
        0.15 * df["indice_ociosidade_urbana"]
    )

    return df
