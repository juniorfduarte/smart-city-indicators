import pandas as pd

from src.censo_urbano.domain.normalization import normalizar


class TestNormalizar:
    def test_min_max_scaling(self):
        prop = pd.Series([0.2, 0.5, 1.0])
        result = normalizar(prop)
        assert result.iloc[0] == 0.0
        assert result.iloc[2] == 1.0
        assert result.iloc[1] == (0.5 - 0.2) / (1.0 - 0.2)

    def test_empate_min_igual_max(self):
        prop = pd.Series([0.5, 0.5, 0.5])
        result = normalizar(prop)
        assert (result == 0.0).all()

    def test_preserva_index(self):
        prop = pd.Series([0.1, 0.9], index=["setor_a", "setor_b"])
        result = normalizar(prop)
        assert list(result.index) == ["setor_a", "setor_b"]

    def test_setor_unico(self):
        prop = pd.Series([0.7], index=["setor_a"])
        result = normalizar(prop)
        assert result.iloc[0] == 0.0
