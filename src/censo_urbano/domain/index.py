import pandas as pd


def calcular_sem_dado(total_domicilios: pd.Series) -> pd.Series:
    """Setor sem_dado: menos de 5 domicílios particulares permanentes ocupados.

    Limiar oficial do IBGE (Censo 2022, "Agregados por Setores Censitários —
    Tratamento de sigilo"): setores com menos de 5 domicílios têm a maioria
    das variáveis omitida, restando só identificação geográfica, número de
    domicílios e população — não dá pra calcular indicadores confiáveis.
    Excluído do cálculo, presente no mapa em cinza.
    """
    return total_domicilios < 5


def calcular_iua(d3: pd.Series, d4: pd.Series) -> pd.Series:
    """Índice_v1(s) = (D3(s) + D4(s)) / 2.

    Setores sem_dado já chegam aqui com D3/D4 = NaN (propagado desde
    domain/indicators.py), então o resultado também é NaN — não é preciso
    tratar sem_dado de novo nesta função.
    """
    return (d3 + d4) / 2
