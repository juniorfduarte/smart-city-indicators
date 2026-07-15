import pandas as pd


def calcular_sem_dado(total_domicilios: pd.Series) -> pd.Series:
    """Setor sem_dado: 0 domicílios — excluído do cálculo, presente no mapa em cinza."""
    return total_domicilios == 0


def calcular_iua(d3: pd.Series, d4: pd.Series) -> pd.Series:
    """Índice_v1(s) = (D3(s) + D4(s)) / 2.

    Setores sem_dado já chegam aqui com D3/D4 = NaN (propagado desde
    domain/indicators.py), então o resultado também é NaN — não é preciso
    tratar sem_dado de novo nesta função.
    """
    return (d3 + d4) / 2
