import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from src.censo_urbano.repositories.malha_repository import carregar_malha_setores

CD_MUN_TESTE = "1234567"


def _quadrado(x, y):
    return Polygon([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)])


@pytest.fixture
def malha_gpkg(tmp_path):
    gdf = gpd.GeoDataFrame(
        {
            "CD_SETOR": ["111111111111111", "222222222222222", "999999999999999"],
            "CD_MUN": ["1234567", "1234567", "9999999"],
            "SITUACAO": ["Urbana", "Rural", "Urbana"],
            "CD_FCU": [".", ".", "."],
            "geometry": [_quadrado(0, 0), _quadrado(1, 0), _quadrado(2, 0)],
        },
        crs="EPSG:4674",
    )
    caminho = tmp_path / "malha_teste.gpkg"
    gdf.to_file(caminho, driver="GPKG")
    return caminho


class TestCarregarMalhaSetores:
    def test_filtra_por_municipio(self, malha_gpkg):
        gdf = carregar_malha_setores(malha_gpkg, cd_mun=CD_MUN_TESTE)
        assert len(gdf) == 2
        assert "999999999999999" not in gdf["CD_SETOR"].values

    def test_colunas_esperadas(self, malha_gpkg):
        gdf = carregar_malha_setores(malha_gpkg, cd_mun=CD_MUN_TESTE)
        assert set(gdf.columns) == {"CD_SETOR", "SITUACAO", "CD_FCU", "geometry"}

    def test_geometria_preservada(self, malha_gpkg):
        gdf = carregar_malha_setores(malha_gpkg, cd_mun=CD_MUN_TESTE)
        setor = gdf[gdf["CD_SETOR"] == "111111111111111"]
        assert setor.geometry.iloc[0].area == pytest.approx(1.0)
