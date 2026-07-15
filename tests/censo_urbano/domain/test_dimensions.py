import pandas as pd
import pytest

from src.censo_urbano.domain.dimensions import calcular_d3, calcular_d4


class TestCalcularD4:
    def test_pesos_redistribuidos(self):
        # agua=1/4, esgoto=1/2, lixo=1/4
        result = calcular_d4(
            ind_agua=pd.Series([1.0]),
            ind_esgoto=pd.Series([0.0]),
            ind_lixo=pd.Series([0.0]),
        )
        assert result.iloc[0] == pytest.approx(0.25)

    def test_todos_indicadores_no_maximo(self):
        result = calcular_d4(
            ind_agua=pd.Series([1.0]),
            ind_esgoto=pd.Series([1.0]),
            ind_lixo=pd.Series([1.0]),
        )
        assert result.iloc[0] == pytest.approx(1.0)


class TestCalcularD3:
    def test_media_dos_tres_indicadores_disponiveis(self):
        result = calcular_d3(
            ind_nao_aglomerado_subnormal=pd.Series([1.0]),
            ind_densidade_banheiro=pd.Series([0.5]),
            ind_especie_adequada=pd.Series([0.0]),
        )
        assert result.iloc[0] == pytest.approx(0.5)

    def test_todos_indicadores_no_minimo(self):
        result = calcular_d3(
            ind_nao_aglomerado_subnormal=pd.Series([0.0]),
            ind_densidade_banheiro=pd.Series([0.0]),
            ind_especie_adequada=pd.Series([0.0]),
        )
        assert result.iloc[0] == pytest.approx(0.0)
