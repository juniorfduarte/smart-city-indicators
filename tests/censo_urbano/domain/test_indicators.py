import pandas as pd
import pytest

from src.censo_urbano.domain.indicators import (
    FaixaBanheiro,
    prop_agua,
    prop_densidade_banheiro,
    prop_esgoto,
    prop_especie_adequada,
    prop_lixo,
)


class TestPropAgua:
    def test_proporcao_basica(self):
        adequados = pd.Series([80.0, 50.0])
        total = pd.Series([100.0, 100.0])
        result = prop_agua(adequados, total)
        assert result.iloc[0] == pytest.approx(0.8)
        assert result.iloc[1] == pytest.approx(0.5)

    def test_setor_sem_domicilios_retorna_nan(self):
        adequados = pd.Series([0.0])
        total = pd.Series([0.0])
        result = prop_agua(adequados, total)
        assert result.isna().all()


class TestPropEsgoto:
    def test_proporcao_basica(self):
        result = prop_esgoto(pd.Series([30.0]), pd.Series([120.0]))
        assert result.iloc[0] == pytest.approx(0.25)


class TestPropLixo:
    def test_proporcao_basica(self):
        result = prop_lixo(pd.Series([90.0]), pd.Series([100.0]))
        assert result.iloc[0] == pytest.approx(0.9)


class TestPropEspecieAdequada:
    def test_proporcao_basica(self):
        result = prop_especie_adequada(pd.Series([70.0]), pd.Series([100.0]))
        assert result.iloc[0] == pytest.approx(0.7)


class TestPropDensidadeBanheiro:
    def test_faixa_unica_adequada(self):
        # 1 banheiro exclusivo, densidade 3 moradores/banheiro <= 4 => adequada
        faixas = [
            FaixaBanheiro(
                nome="1_banheiro",
                domicilios=pd.Series([10.0]),
                moradores=pd.Series([30.0]),
                num_banheiros=1,
            ),
        ]
        total = pd.Series([10.0])
        result = prop_densidade_banheiro(faixas, total)
        assert result.iloc[0] == pytest.approx(1.0)

    def test_faixa_inadequada_por_densidade(self):
        # 1 banheiro exclusivo, densidade 5 moradores/banheiro > 4 => inadequada
        faixas = [
            FaixaBanheiro(
                nome="1_banheiro",
                domicilios=pd.Series([10.0]),
                moradores=pd.Series([50.0]),
                num_banheiros=1,
            ),
        ]
        total = pd.Series([10.0])
        result = prop_densidade_banheiro(faixas, total)
        assert result.iloc[0] == pytest.approx(0.0)

    def test_faixa_sem_banheiro_exclusivo_sempre_inadequada(self):
        faixas = [
            FaixaBanheiro(
                nome="nenhum",
                domicilios=pd.Series([10.0]),
                moradores=pd.Series([5.0]),
                num_banheiros=None,
            ),
        ]
        total = pd.Series([10.0])
        result = prop_densidade_banheiro(faixas, total)
        assert result.iloc[0] == pytest.approx(0.0)

    def test_mistura_de_faixas(self):
        faixas = [
            FaixaBanheiro(
                nome="1_banheiro",
                domicilios=pd.Series([6.0]),
                moradores=pd.Series([12.0]),  # densidade 2 => adequada
                num_banheiros=1,
            ),
            FaixaBanheiro(
                nome="4_mais",
                domicilios=pd.Series([2.0]),
                moradores=pd.Series([40.0]),  # densidade 5 (piso 4 banheiros) => inadequada
                num_banheiros=4,
            ),
            FaixaBanheiro(
                nome="sem_banheiro",
                domicilios=pd.Series([2.0]),
                moradores=pd.Series([4.0]),
                num_banheiros=None,
            ),
        ]
        total = pd.Series([10.0])
        result = prop_densidade_banheiro(faixas, total)
        assert result.iloc[0] == pytest.approx(0.6)

    def test_setor_sem_domicilios_retorna_nan(self):
        faixas = [
            FaixaBanheiro(
                nome="1_banheiro",
                domicilios=pd.Series([0.0]),
                moradores=pd.Series([0.0]),
                num_banheiros=1,
            ),
        ]
        total = pd.Series([0.0])
        result = prop_densidade_banheiro(faixas, total)
        assert result.isna().all()
