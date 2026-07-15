import pandas as pd


def normalizar(prop: pd.Series) -> pd.Series:
    """Ind(i,s) = (prop(i,s) - min_U) / (max_U - min_U).

    Se min_U == max_U (todos os setores empatados), retorna 0.0 para todos —
    não há variação relativa a capturar no universo de comparação.
    """
    min_val = prop.min()
    max_val = prop.max()
    if max_val == min_val:
        return pd.Series(0.0, index=prop.index)
    return (prop - min_val) / (max_val - min_val)
