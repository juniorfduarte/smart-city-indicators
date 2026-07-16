from pydantic import BaseModel


class SetorIUA(BaseModel):
    """Índice Urbano Aberto (IUA) e dimensões intermediárias de um setor censitário.

    d3, d4 e iua são None quando sem_dado=True (setor sem domicílios, ver
    domain/index.py) ou quando o IBGE suprimiu variáveis suficientes para
    zerar um denominador do setor.
    """

    cd_setor: str
    sem_dado: bool
    d3: float | None
    d4: float | None
    iua: float | None
