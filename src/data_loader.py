import pandas as pd
from pathlib import Path
import unicodedata

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dados_ibge_pr.xlsx"


def normalizar_texto(texto: str) -> str:
    return (
        unicodedata.normalize("NFKD", texto)
        .encode("ASCII", "ignore")
        .decode("ASCII")
        .lower()
    )


def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH, header=1)

    df.columns = df.iloc[0]
    df = df[1:]

    df = df.rename(columns={
        'Município [-]': 'municipio',
        'Área Territorial - km² [2024]': 'area_km2',
        'População no último censo - pessoas [2022]': 'populacao',
        'Densidade demográfica - hab/km² [2022]': 'densidade',
        'PIB per capita - R$ [2023]': 'pib_per_capita',
        'IDHM <span>Índice de desenvolvimento humano municipal</span> [2010]': 'idhm'
    })

    df = df[['municipio', 'area_km2', 'populacao', 'densidade', 'pib_per_capita', 'idhm']]

    df["municipio"] = df["municipio"] = df["municipio"].str.strip()
    df["municipio_normalizado"] = df["municipio"].apply(normalizar_texto)
    df['area_km2'] = pd.to_numeric(df['area_km2'], errors='coerce')
    df['populacao'] = pd.to_numeric(df['populacao'], errors='coerce')
    df['densidade'] = pd.to_numeric(df['densidade'], errors='coerce')
    df['pib_per_capita'] = pd.to_numeric(df['pib_per_capita'], errors='coerce')
    df['idhm'] = pd.to_numeric(df['idhm'], errors='coerce')

    return df
