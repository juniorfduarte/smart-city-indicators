from unittest.mock import MagicMock


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


class TestCidades:
    def test_lista_todas(self, client):
        response = client.get("/cidades")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_busca_por_nome(self, client):
        response = client.get("/cidades?nome=mar")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["municipio"] == "Maringá"

    def test_nome_muito_curto_retorna_422(self, client):
        response = client.get("/cidades?nome=m")
        assert response.status_code == 422

    def test_cidade_por_slug_encontrada(self, client):
        response = client.get("/cidades/maringa")
        assert response.status_code == 200
        assert response.json()["municipio"] == "Maringá"

    def test_cidade_por_slug_nao_encontrada(self, client):
        response = client.get("/cidades/naoexiste")
        assert response.status_code == 404


class TestRankings:
    def test_ranking_pib_ordem(self, client):
        response = client.get("/ranking/pib")
        assert response.status_code == 200
        data = response.json()
        assert data[0]["municipio"] == "Curitiba"
        assert data[0]["pib_per_capita"] == 75000.0

    def test_ranking_pib_top_n(self, client):
        response = client.get("/ranking/pib?top_n=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_ranking_pib_top_n_zero_invalido(self, client):
        assert client.get("/ranking/pib?top_n=0").status_code == 422

    def test_ranking_pib_top_n_acima_limite_invalido(self, client):
        assert client.get("/ranking/pib?top_n=101").status_code == 422

    def test_ranking_idhm_ordem(self, client):
        data = client.get("/ranking/idhm").json()
        assert data[0]["municipio"] == "Curitiba"

    def test_ranking_densidade_ordem(self, client):
        data = client.get("/ranking/densidade").json()
        assert data[0]["municipio"] == "Curitiba"


class TestMaringaIndicadores:
    def test_lista_todos(self, client):
        response = client.get("/maringa/indicadores")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_filtro_bairro(self, client):
        response = client.get("/maringa/indicadores?bairro=Centro")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(d["bairro"] == "Centro" for d in data)

    def test_filtro_zona(self, client):
        response = client.get("/maringa/indicadores?zona=Norte")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_por_bairro_agrupado(self, client):
        response = client.get("/maringa/indicadores/bairro")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert "smart_city_score" in data[0]


class TestIBGE:
    def test_lista_municipios_pr(self, client):
        response = client.get("/ibge/pr/municipios")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_municipio_por_id(self, client):
        response = client.get("/ibge/pr/municipios/4115200")
        assert response.status_code == 200

    def test_municipio_ibge_error_retorna_502(self, client):
        from src.api import app, get_ibge_loader

        mock_error = MagicMock()
        mock_error.get_municipio_por_id.side_effect = RuntimeError("IBGE fora do ar")
        app.dependency_overrides[get_ibge_loader] = lambda: mock_error

        try:
            response = client.get("/ibge/pr/municipios/9999999")
            assert response.status_code == 502
        finally:
            del app.dependency_overrides[get_ibge_loader]
