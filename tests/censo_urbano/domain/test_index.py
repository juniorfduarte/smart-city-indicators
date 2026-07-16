import numpy as np
import pandas as pd
import pytest

from src.censo_urbano.domain.index import calcular_iua, calcular_sem_dado


class TestCalcularSemDado:
    def test_setor_com_zero_domicilios_e_sem_dado(self):
        total = pd.Series([0.0, 10.0])
        result = calcular_sem_dado(total)
        assert result.iloc[0]
        assert not result.iloc[1]

    def test_setor_com_menos_de_cinco_domicilios_e_sem_dado(self):
        # Limiar oficial do IBGE: setores com < 5 domicílios têm quase tudo suprimido.
        total = pd.Series([1.0, 4.0])
        result = calcular_sem_dado(total)
        assert result.iloc[0]
        assert result.iloc[1]

    def test_setor_com_cinco_ou_mais_domicilios_nao_e_sem_dado(self):
        total = pd.Series([5.0, 100.0])
        result = calcular_sem_dado(total)
        assert not result.iloc[0]
        assert not result.iloc[1]


class TestCalcularIua:
    def test_media_simples_d3_d4(self):
        result = calcular_iua(d3=pd.Series([0.8]), d4=pd.Series([0.4]))
        assert result.iloc[0] == pytest.approx(0.6)

    def test_propaga_nan_de_setor_sem_dado(self):
        result = calcular_iua(d3=pd.Series([np.nan]), d4=pd.Series([0.5]))
        assert result.isna().all()
