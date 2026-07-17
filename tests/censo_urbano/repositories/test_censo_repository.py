import pandas as pd
import pytest

from src.censo_urbano.repositories.censo_repository import (
    carregar_setores,
    ler_basico,
    ler_domicilio1,
    ler_domicilio2,
    ler_domicilio3,
)

CD_MUN_TESTE = "1234567"


def _escrever(caminho, conteudo):
    caminho.write_text(conteudo, encoding="latin1")


@pytest.fixture
def basico_csv(tmp_path):
    caminho = tmp_path / "basico.csv"
    _escrever(
        caminho,
        '"CD_SETOR";"CD_MUN";"NM_MUN";"v0001";"v0007"\r\n'
        '"111111111111111";"1234567";"Maringá";"100";"30"\r\n'
        '"222222222222222";"1234567";"Maringá";"50";"15"\r\n'
        '"333333333333333";"1234567";"Maringá";"0";"0"\r\n'
        '"999999999999999";"9999999";"Outra Cidade";"999";"999"\r\n',
    )
    return caminho


@pytest.fixture
def domicilio1_csv(tmp_path):
    caminho = tmp_path / "domicilio1.csv"
    _escrever(
        caminho,
        '"CD_setor";"V00047"\r\n'
        '"111111111111111";"25"\r\n'
        '"222222222222222";"X"\r\n',
    )
    return caminho


@pytest.fixture
def domicilio2_csv(tmp_path):
    caminho = tmp_path / "domicilio2.csv"
    _escrever(
        caminho,
        '"setor";"V00111"\r\n'
        '"111111111111111";"20"\r\n'
        '"222222222222222";"10"\r\n',
    )
    return caminho


@pytest.fixture
def domicilio3_csv(tmp_path):
    caminho = tmp_path / "domicilio3.csv"
    _escrever(
        caminho,
        '"setor";"V00552"\r\n'
        '"111111111111111";"60"\r\n'
        '"222222222222222";"30"\r\n',
    )
    return caminho


class TestLerBasico:
    def test_filtra_por_municipio(self, basico_csv):
        df = ler_basico(basico_csv, cd_mun=CD_MUN_TESTE)
        assert len(df) == 3
        assert "999999999999999" not in df["CD_SETOR"].values

    def test_decodifica_latin1(self, basico_csv):
        df = ler_basico(basico_csv, cd_mun=CD_MUN_TESTE)
        assert (df["NM_MUN"] == "Maringá").all()

    def test_mantem_setor_sem_domicilios(self, basico_csv):
        df = ler_basico(basico_csv, cd_mun=CD_MUN_TESTE)
        setor_vazio = df[df["CD_SETOR"] == "333333333333333"]
        assert setor_vazio["v0007"].iloc[0] == 0


class TestLerDomicilios:
    def test_domicilio1_normaliza_coluna_setor(self, domicilio1_csv):
        df = ler_domicilio1(domicilio1_csv)
        assert "CD_SETOR" in df.columns
        assert "CD_setor" not in df.columns

    def test_domicilio1_trata_x_como_ausente(self, domicilio1_csv):
        df = ler_domicilio1(domicilio1_csv)
        valor = df.loc[df["CD_SETOR"] == "222222222222222", "V00047"].iloc[0]
        assert pd.isna(valor)

    def test_domicilio2_normaliza_coluna_setor(self, domicilio2_csv):
        df = ler_domicilio2(domicilio2_csv)
        assert "CD_SETOR" in df.columns

    def test_domicilio3_normaliza_coluna_setor(self, domicilio3_csv):
        df = ler_domicilio3(domicilio3_csv)
        assert "CD_SETOR" in df.columns


class TestCarregarSetores:
    def test_junta_as_quatro_tabelas(
        self, basico_csv, domicilio1_csv, domicilio2_csv, domicilio3_csv
    ):
        df = carregar_setores(
            basico_csv, domicilio1_csv, domicilio2_csv, domicilio3_csv, cd_mun=CD_MUN_TESTE
        )
        assert len(df) == 3
        assert {"V00047", "V00111", "V00552"} <= set(df.columns)

    def test_setor_sem_domicilios_vira_nan_nas_colunas_de_caracteristicas(
        self, basico_csv, domicilio1_csv, domicilio2_csv, domicilio3_csv
    ):
        df = carregar_setores(
            basico_csv, domicilio1_csv, domicilio2_csv, domicilio3_csv, cd_mun=CD_MUN_TESTE
        )
        setor_vazio = df[df["CD_SETOR"] == "333333333333333"]
        assert setor_vazio["V00047"].isna().all()
        assert setor_vazio["V00111"].isna().all()
        assert setor_vazio["V00552"].isna().all()

    def test_valores_normais_preservados(
        self, basico_csv, domicilio1_csv, domicilio2_csv, domicilio3_csv
    ):
        df = carregar_setores(
            basico_csv, domicilio1_csv, domicilio2_csv, domicilio3_csv, cd_mun=CD_MUN_TESTE
        )
        setor = df[df["CD_SETOR"] == "111111111111111"]
        assert setor["V00047"].iloc[0] == 25
        assert setor["V00111"].iloc[0] == 20
        assert setor["V00552"].iloc[0] == 60
