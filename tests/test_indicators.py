import pandas as pd
import pytest

from src.indicators import ranking_densidade, ranking_idhm, ranking_pib


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "municipio": ["Cidade A", "Cidade B", "Cidade C"],
        "pib_per_capita": [50000.0, 30000.0, 70000.0],
        "idhm": [0.80, 0.75, 0.85],
        "densidade": [1000.0, 500.0, 2000.0],
    })


class TestRankingPib:
    def test_order(self, sample_df):
        result = ranking_pib(sample_df, top_n=3)
        assert result[0]["municipio"] == "Cidade C"
        assert result[1]["municipio"] == "Cidade A"
        assert result[2]["municipio"] == "Cidade B"

    def test_top_n_limit(self, sample_df):
        assert len(ranking_pib(sample_df, top_n=2)) == 2

    def test_fields_returned(self, sample_df):
        result = ranking_pib(sample_df, top_n=1)
        assert set(result[0].keys()) == {"municipio", "pib_per_capita"}


class TestRankingIdhm:
    def test_order(self, sample_df):
        result = ranking_idhm(sample_df, top_n=3)
        assert result[0]["municipio"] == "Cidade C"
        assert result[1]["municipio"] == "Cidade A"

    def test_fields_returned(self, sample_df):
        result = ranking_idhm(sample_df, top_n=1)
        assert set(result[0].keys()) == {"municipio", "idhm"}


class TestRankingDensidade:
    def test_order(self, sample_df):
        result = ranking_densidade(sample_df, top_n=3)
        assert result[0]["municipio"] == "Cidade C"
        assert result[0]["densidade"] == 2000.0

    def test_fields_returned(self, sample_df):
        result = ranking_densidade(sample_df, top_n=1)
        assert set(result[0].keys()) == {"municipio", "densidade"}
