from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient

MOCK_DF = pd.DataFrame({
    "municipio": ["Maringá", "Curitiba", "Londrina"],
    "municipio_normalizado": ["maringa", "curitiba", "londrina"],
    "area_km2": [487.93, 435.27, 1653.0],
    "populacao": [430157.0, 1963726.0, 578049.0],
    "densidade": [881.8, 4517.0, 350.0],
    "pib_per_capita": [55000.0, 75000.0, 45000.0],
    "idhm": [0.808, 0.823, 0.778],
})

MOCK_MARINGA_DF = pd.DataFrame({
    "bairro": ["Centro", "Zona 07", "Centro"],
    "zona": ["Sul", "Norte", "Sul"],
    "smart_city_score": [0.75, 0.60, 0.80],
    "indice_qualidade_urbana": [0.70, 0.55, 0.72],
    "indice_infraestrutura_urbana": [0.80, 0.65, 0.82],
    "indice_adensamento_inteligente": [0.50, 0.45, 0.55],
})

MOCK_IBGE_DF = pd.DataFrame({
    "id": [4115200, 4106902],
    "nome": ["Maringá", "Curitiba"],
})

MOCK_SETORES_IUA_DF = pd.DataFrame({
    "CD_SETOR": ["111", "222"],
    "sem_dado": [False, False],
    "d3": [0.8, 0.4],
    "d4": [0.6, 0.2],
    "iua": [0.7, 0.3],
})

MOCK_SETORES_IUA_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-51.94, -23.42], [-51.94, -23.41],
                    [-51.93, -23.41], [-51.93, -23.42], [-51.94, -23.42],
                ]],
            },
            "properties": {"CD_SETOR": "111", "sem_dado": False, "d3": 0.8, "d4": 0.6, "iua": 0.7},
        },
    ],
}


@pytest.fixture
def client():
    mock_loader = MagicMock()
    mock_loader.get_municipios_por_estado.return_value = MOCK_IBGE_DF
    mock_loader.get_municipio_por_id.return_value = MOCK_IBGE_DF.head(1)

    with (
        patch("src.api.load_data", return_value=MOCK_DF),
        patch("src.api.load_maringa_data", return_value=MOCK_MARINGA_DF),
        patch("src.api.load_setores_iua", return_value=MOCK_SETORES_IUA_DF),
        patch("src.api.load_setores_iua_geojson", return_value=MOCK_SETORES_IUA_GEOJSON),
    ):
        from src.api import app, get_df, get_ibge_loader, get_maringa_df
        from src.censo_urbano.api.router import get_setores_iua, get_setores_iua_geojson

        app.dependency_overrides[get_df] = lambda: MOCK_DF
        app.dependency_overrides[get_maringa_df] = lambda: MOCK_MARINGA_DF
        app.dependency_overrides[get_ibge_loader] = lambda: mock_loader
        app.dependency_overrides[get_setores_iua] = lambda: MOCK_SETORES_IUA_DF
        app.dependency_overrides[get_setores_iua_geojson] = lambda: MOCK_SETORES_IUA_GEOJSON

        with TestClient(app) as c:
            yield c

    app.dependency_overrides.clear()
