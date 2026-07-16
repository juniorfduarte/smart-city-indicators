import numpy as np
import pandas as pd
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.censo_urbano.api.router import get_setores_iua, router

MOCK_DF = pd.DataFrame({
    "CD_SETOR": ["111", "222", "333"],
    "sem_dado": [False, False, True],
    "d3": [0.8, 0.4, np.nan],
    "d4": [0.6, 0.2, np.nan],
    "iua": [0.7, 0.3, np.nan],
})


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_setores_iua] = lambda: MOCK_DF

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


class TestListarSetores:
    def test_retorna_todos_os_setores(self, client):
        response = client.get("/iua/setores")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_setor_sem_dado_tem_indices_nulos(self, client):
        response = client.get("/iua/setores")
        setor = next(s for s in response.json() if s["cd_setor"] == "333")
        assert setor["sem_dado"] is True
        assert setor["d3"] is None
        assert setor["d4"] is None
        assert setor["iua"] is None


class TestObterSetor:
    def test_retorna_setor_especifico(self, client):
        response = client.get("/iua/setores/111")
        assert response.status_code == 200
        body = response.json()
        assert body["cd_setor"] == "111"
        assert body["d3"] == pytest.approx(0.8)

    def test_setor_inexistente_retorna_404(self, client):
        response = client.get("/iua/setores/999")
        assert response.status_code == 404
