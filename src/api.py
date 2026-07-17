import logging
from contextlib import asynccontextmanager
from typing import Annotated

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from starlette.middleware.cors import CORSMiddleware

from src.censo_urbano.api.router import router as iua_router
from src.censo_urbano.config import (
    BASICO_PATH,
    DOMICILIO1_PATH,
    DOMICILIO2_PATH,
    DOMICILIO3_PATH,
)
from src.censo_urbano.repositories.censo_repository import carregar_setores
from src.censo_urbano.services.iua_service import calcular_iua_setores
from src.config import CORS_ORIGINS
from src.data_loader import load_data
from src.ibge_data_loader import IBGEDataLoader
from src.indicators import ranking_densidade, ranking_idhm, ranking_pib
from src.maringa_data_loader import load_maringa_data
from src.utils import normalizar_texto


def load_setores_iua() -> pd.DataFrame:
    df_setores = carregar_setores(
        BASICO_PATH, DOMICILIO1_PATH, DOMICILIO2_PATH, DOMICILIO3_PATH
    )
    return calcular_iua_setores(df_setores)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Carregando dados...")
    app.state.df = load_data()
    app.state.df_maringa = load_maringa_data()
    app.state.ibge_loader = IBGEDataLoader()
    app.state.setores_iua = load_setores_iua()
    logger.info("Dados carregados com sucesso.")
    yield
    logger.info("Encerrando aplicação.")


app = FastAPI(
    title="Smart City Indicators API",
    description="API de indicadores urbanos para Maringá-PR. Desenvolvido por Francisco Junior.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(iua_router)


def get_df(request: Request) -> pd.DataFrame:
    return request.app.state.df


def get_maringa_df(request: Request) -> pd.DataFrame:
    return request.app.state.df_maringa


def get_ibge_loader(request: Request) -> IBGEDataLoader:
    return request.app.state.ibge_loader


DfDep = Annotated[pd.DataFrame, Depends(get_df)]
MaringaDfDep = Annotated[pd.DataFrame, Depends(get_maringa_df)]
IBGELoaderDep = Annotated[IBGEDataLoader, Depends(get_ibge_loader)]


@app.get("/")
def root() -> dict:
    return {"message": "Smart City Indicators API", "docs": "/docs"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/cidades")
def get_cidades(
    df: DfDep,
    nome: str | None = Query(None, min_length=2, max_length=100),
) -> list[dict]:
    if nome:
        nome_norm = normalizar_texto(nome)
        result = df[df["municipio_normalizado"].str.contains(nome_norm, na=False)]
        return result.to_dict(orient="records")
    return df.to_dict(orient="records")


@app.get("/cidades/{nome}")
def get_cidade(nome: str, df: DfDep) -> dict:
    nome_norm = normalizar_texto(nome)
    result = df[df["municipio_normalizado"].str.contains(nome_norm, na=False)]
    if result.empty:
        raise HTTPException(status_code=404, detail="Cidade não encontrada")
    return result.to_dict(orient="records")[0]


@app.get("/ranking/pib")
def get_ranking_pib(
    df: DfDep,
    top_n: int = Query(10, ge=1, le=100),
) -> list[dict]:
    return ranking_pib(df, top_n)


@app.get("/ranking/idhm")
def get_ranking_idhm(
    df: DfDep,
    top_n: int = Query(10, ge=1, le=100),
) -> list[dict]:
    return ranking_idhm(df, top_n)


@app.get("/ranking/densidade")
def get_ranking_densidade(
    df: DfDep,
    top_n: int = Query(10, ge=1, le=100),
) -> list[dict]:
    return ranking_densidade(df, top_n)


@app.get("/ibge/pr/municipios")
def list_ibge_pr_municipios(loader: IBGELoaderDep) -> list[dict]:
    resultado = loader.get_municipios_por_estado("PR")
    return resultado.fillna("").to_dict(orient="records")


@app.get("/ibge/pr/municipios/{municipio_id}")
def get_ibge_pr_municipio(municipio_id: int, loader: IBGELoaderDep) -> list[dict]:
    try:
        resultado = loader.get_municipio_por_id(municipio_id)
        return resultado.to_dict(orient="records")
    except RuntimeError:
        raise HTTPException(status_code=502, detail="Erro ao consultar API do IBGE")


@app.get("/maringa/indicadores")
def get_indicadores(
    df_maringa: MaringaDfDep,
    bairro: str | None = Query(None, max_length=100),
    zona: str | None = Query(None, max_length=50),
) -> list[dict]:
    result = df_maringa.copy()
    if bairro:
        result = result[result["bairro"].str.lower() == bairro.lower()]
    if zona:
        result = result[result["zona"].str.lower() == zona.lower()]
    return result.to_dict(orient="records")


@app.get("/maringa/indicadores/bairro")
def indicadores_por_bairro(df_maringa: MaringaDfDep) -> list[dict]:
    result = (
        df_maringa.groupby("bairro")[[
            "smart_city_score",
            "indice_qualidade_urbana",
            "indice_infraestrutura_urbana",
            "indice_adensamento_inteligente",
        ]]
        .mean()
        .reset_index()
        .sort_values(by="smart_city_score", ascending=False)
    )
    return result.to_dict(orient="records")
