from pathlib import Path

import geopandas as gpd

from src.censo_urbano.config import CD_MUN_MARINGA


def carregar_malha_setores(caminho: Path, cd_mun: str = CD_MUN_MARINGA) -> gpd.GeoDataFrame:
    """Geometria dos setores censitários de um município.

    Só CD_SETOR + geometry: o export real de Maringá (malha_maringa.gpkg) não
    traz CD_MUN nem atributos (SITUACAO, CD_FCU) — já vem pré-filtrado para o
    município. Se o arquivo tiver CD_MUN (ex.: extração de um estado inteiro),
    filtra por ele; caso contrário assume que já está filtrado.

    CD_FCU (aglomerado subnormal) não vem mais desta malha: já está disponível
    em `censo_repository.carregar_setores` via o arquivo básico (mesma fonte,
    sem precisar de um segundo cruzamento espacial — ver iua_service.py).
    """
    gdf = gpd.read_file(caminho)
    if "CD_MUN" in gdf.columns:
        gdf = gdf[gdf["CD_MUN"].astype(str) == cd_mun].reset_index(drop=True)
    return gdf[["CD_SETOR", "geometry"]]
