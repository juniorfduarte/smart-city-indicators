from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request

from src.censo_urbano.schemas.setor import SetorIUA

router = APIRouter(prefix="/iua", tags=["IUA"])


def get_setores_iua(request: Request) -> pd.DataFrame:
    return request.app.state.setores_iua


SetoresIUADep = Annotated[pd.DataFrame, Depends(get_setores_iua)]


def _valor_ou_none(valor: float) -> float | None:
    return None if pd.isna(valor) else float(valor)


def _linha_para_schema(linha: pd.Series) -> SetorIUA:
    return SetorIUA(
        cd_setor=linha["CD_SETOR"],
        sem_dado=bool(linha["sem_dado"]),
        d3=_valor_ou_none(linha["d3"]),
        d4=_valor_ou_none(linha["d4"]),
        iua=_valor_ou_none(linha["iua"]),
    )


@router.get("/setores")
def listar_setores(df: SetoresIUADep) -> list[SetorIUA]:
    return [_linha_para_schema(linha) for _, linha in df.iterrows()]


@router.get("/setores/{cd_setor}")
def obter_setor(cd_setor: str, df: SetoresIUADep) -> SetorIUA:
    resultado = df[df["CD_SETOR"] == cd_setor]
    if resultado.empty:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    return _linha_para_schema(resultado.iloc[0])
