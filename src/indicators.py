import pandas as pd


def ranking_pib(df, top_n=10):
    return (
        df.sort_values(by="pib_per_capita", ascending=False)
        .head(top_n)
        [["municipio", "pib_per_capita"]]
        .to_dict(orient="records")
    )


def ranking_idhm(df, top_n=10):
    return (
        df.sort_values(by="idhm", ascending=False)
        .head(top_n)
        [["municipio", "idhm"]]
        .to_dict(orient="records")
    )


def ranking_densidade(df, top_n=10):
    return (
        df.sort_values(by="densidade", ascending=False)
        .head(top_n)
        [["municipio", "densidade"]]
        .to_dict(orient="records")
    )


def normalizar(df: pd.DataFrame, coluna: str) -> pd.Series:
    return (df[coluna] - df[coluna].min()) / (df[coluna].max() - df[coluna].min())


def calcular_indicadores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    print(df.columns.tolist())

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
