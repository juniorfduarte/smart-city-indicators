import pandas as pd
import pytest

from src.maringa_data_loader import normalizar, to_snake_case


class TestNormalizar:
    def test_min_is_zero_max_is_one(self):
        df = pd.DataFrame({"col": [0.0, 50.0, 100.0]})
        result = normalizar(df, "col")
        assert result.iloc[0] == 0.0
        assert result.iloc[2] == 1.0
        assert result.iloc[1] == pytest.approx(0.5)

    def test_all_equal_returns_zero(self):
        df = pd.DataFrame({"col": [5.0, 5.0, 5.0]})
        result = normalizar(df, "col")
        assert list(result) == [0.0, 0.0, 0.0]

    def test_preserves_index(self):
        df = pd.DataFrame({"col": [10.0, 20.0]}, index=[5, 10])
        result = normalizar(df, "col")
        assert list(result.index) == [5, 10]


class TestToSnakeCase:
    def test_spaces_to_underscore(self):
        assert to_snake_case("Inst Saude") == "inst_saude"

    def test_strips_and_lowercases(self):
        assert to_snake_case("  Densidade  ") == "densidade"

    def test_removes_special_chars(self):
        assert to_snake_case("Valor (m²)") == "valor_m"

    def test_already_snake_case(self):
        assert to_snake_case("bairro") == "bairro"
