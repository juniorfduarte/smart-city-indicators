from pathlib import Path

import geopandas as gpd

from src.censo_urbano.config import CD_MUN_MARINGA


def carregar_malha_setores(caminho: Path, cd_mun: str = CD_MUN_MARINGA) -> gpd.GeoDataFrame:
    """Geometria dos setores censitários de um município.

    CD_FCU vem pronto no arquivo (aglomerado subnormal) — em Maringá está vazio
    ("." ) para todos os setores, ver spec §6.2 (atualização 2026-07-16): não há
    aglomerado subnormal delimitado pelo IBGE na cidade, não precisa de
    cruzamento espacial com uma malha separada de favelas.
    """
    gdf = gpd.read_file(caminho)
    gdf["CD_MUN"] = gdf["CD_MUN"].astype(str)
    gdf = gdf[gdf["CD_MUN"] == cd_mun].reset_index(drop=True)
    return gdf[["CD_SETOR", "SITUACAO", "CD_FCU", "geometry"]]
