from dataclasses import dataclass

import pandas as pd

from src.censo_urbano.config import LIMIAR_DENSIDADE_BANHEIRO


def _prop(domicilios_adequados: pd.Series, total_domicilios: pd.Series) -> pd.Series:
    """prop(i,s) = domicílios em condição adequada / total de domicílios no setor s.

    Setores com total_domicilios == 0 retornam NaN (sem_dado — ver domain/index.py),
    em vez de propagar uma divisão por zero.
    """
    return (domicilios_adequados / total_domicilios).where(total_domicilios != 0)


def prop_agua(domicilios_adequados: pd.Series, domicilios_total_abastecimento: pd.Series) -> pd.Series:
    return _prop(domicilios_adequados, domicilios_total_abastecimento)


def prop_esgoto(domicilios_adequados: pd.Series, total_domicilios: pd.Series) -> pd.Series:
    return _prop(domicilios_adequados, total_domicilios)


def prop_lixo(domicilios_adequados: pd.Series, total_domicilios: pd.Series) -> pd.Series:
    return _prop(domicilios_adequados, total_domicilios)


def prop_especie_adequada(domicilios_adequados: pd.Series, domicilios_total_especie: pd.Series) -> pd.Series:
    return _prop(domicilios_adequados, domicilios_total_especie)


@dataclass(frozen=True)
class FaixaBanheiro:
    """Uma faixa de domicílios por número de banheiros (§6.3 do spec).

    num_banheiros=None identifica faixas sem banheiro exclusivo (comum,
    sanitário/buraco, nenhum) — sempre inadequadas, não entram no cálculo de
    densidade. Para a faixa "4+", o chamador já deve passar o piso conservador
    (PISO_BANHEIROS_FAIXA_4_MAIS = 4).
    """

    nome: str
    domicilios: pd.Series
    moradores: pd.Series
    num_banheiros: int | None


def prop_densidade_banheiro(faixas: list[FaixaBanheiro], total_domicilios: pd.Series) -> pd.Series:
    """§6.3: aproximação por faixa agregada (não é o cálculo domicílio-a-domicílio do IBEU).

    Cada faixa com banheiro exclusivo é tratada como homogênea internamente:
    densidade_média(f) = moradores_na_faixa(f) / (domicílios_na_faixa(f) × nº_banheiros(f))
    Faixa adequada se densidade_média(f) <= LIMIAR_DENSIDADE_BANHEIRO.
    """
    domicilios_adequados = pd.Series(0.0, index=total_domicilios.index)
    for faixa in faixas:
        if faixa.num_banheiros is None:
            continue
        densidade_media = faixa.moradores / (faixa.domicilios * faixa.num_banheiros)
        adequada = densidade_media <= LIMIAR_DENSIDADE_BANHEIRO
        domicilios_adequados = domicilios_adequados + faixa.domicilios.where(adequada, 0.0)
    return _prop(domicilios_adequados, total_domicilios)
