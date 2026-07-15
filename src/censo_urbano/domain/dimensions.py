import pandas as pd

from src.censo_urbano.config import (
    PESO_AGUA_D4,
    PESO_DENSIDADE_BANHEIRO_D3,
    PESO_ESGOTO_D4,
    PESO_ESPECIE_ADEQUADA_D3,
    PESO_LIXO_D4,
    PESO_NAO_AGLOMERADO_SUBNORMAL_D3,
)


def calcular_d4(ind_agua: pd.Series, ind_esgoto: pd.Series, ind_lixo: pd.Series) -> pd.Series:
    """D4(s) = água·1/4 + esgoto·1/2 + lixo·1/4 (pesos redistribuídos, energia N/A)."""
    return PESO_AGUA_D4 * ind_agua + PESO_ESGOTO_D4 * ind_esgoto + PESO_LIXO_D4 * ind_lixo


def calcular_d3(
    ind_nao_aglomerado_subnormal: pd.Series,
    ind_densidade_banheiro: pd.Series,
    ind_especie_adequada: pd.Series,
) -> pd.Series:
    """D3(s) = média dos 3 indicadores disponíveis (parede e dormitório N/A, peso redistribuído)."""
    return (
        PESO_NAO_AGLOMERADO_SUBNORMAL_D3 * ind_nao_aglomerado_subnormal
        + PESO_DENSIDADE_BANHEIRO_D3 * ind_densidade_banheiro
        + PESO_ESPECIE_ADEQUADA_D3 * ind_especie_adequada
    )
