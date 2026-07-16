import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from src.censo_urbano.repositories.malha_repository import carregar_malha_setores

CD_MUN_TESTE = "1234567"


def _quadrado(x, y):
    return Polygon([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)])


@pytest.fixture
def malha_gpkg_com_cd_mun(tmp_path):
    gdf = gpd.GeoDataFrame(
        {
            "CD_SETOR": ["111111111111111", "222222222222222", "999999999999999"],
            "CD_MUN": ["1234567", "1234567", "9999999"],
            "geometry": [_quadrado(0, 0), _quadrado(1, 0), _quadrado(2, 0)],
        },
        crs="EPSG:4674",
    )
    caminho = tmp_path / "malha_teste.gpkg"
    gdf.to_file(caminho, driver="GPKG")
    return caminho


@pytest.fixture
def malha_gpkg_ja_filtrado(tmp_path):
    # Formato real do arquivo de Maringá: só CD_SETOR + geometry, sem CD_MUN
    # (o export já vem pré-filtrado para o município).
    gdf = gpd.GeoDataFrame(
        {
            "CD_SETOR": ["111111111111111", "222222222222222"],
            "geometry": [_quadrado(0, 0), _quadrado(1, 0)],
        },
        crs="EPSG:4674",
    )
    caminho = tmp_path / "malha_ja_filtrada.gpkg"
    gdf.to_file(caminho, driver="GPKG")
    return caminho


class TestCarregarMalhaSetores:
    def test_filtra_por_municipio_quando_cd_mun_presente(self, malha_gpkg_com_cd_mun):
        gdf = carregar_malha_setores(malha_gpkg_com_cd_mun, cd_mun=CD_MUN_TESTE)
        assert len(gdf) == 2
        assert "999999999999999" not in gdf["CD_SETOR"].values

    def test_colunas_esperadas(self, malha_gpkg_com_cd_mun):
        gdf = carregar_malha_setores(malha_gpkg_com_cd_mun, cd_mun=CD_MUN_TESTE)
        assert set(gdf.columns) == {"CD_SETOR", "geometry"}

    def test_geometria_preservada(self, malha_gpkg_com_cd_mun):
        gdf = carregar_malha_setores(malha_gpkg_com_cd_mun, cd_mun=CD_MUN_TESTE)
        setor = gdf[gdf["CD_SETOR"] == "111111111111111"]
        assert setor.geometry.iloc[0].area == pytest.approx(1.0)

    def test_arquivo_sem_cd_mun_nao_filtra(self, malha_gpkg_ja_filtrado):
        gdf = carregar_malha_setores(malha_gpkg_ja_filtrado, cd_mun=CD_MUN_TESTE)
        assert len(gdf) == 2
        assert set(gdf.columns) == {"CD_SETOR", "geometry"}
