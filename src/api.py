from fastapi import FastAPI, Query
from src.data_loader import load_data
from src.utils import normalizar_texto
from src.indicators import ranking_pib, ranking_idhm, ranking_densidade
from src.maringa_data_loader import load_maringa_data
from fastapi import HTTPException
from src.IBGE_data_loarder import IBGEDataLoader

app = FastAPI()
df = load_data()
df_maringa = load_maringa_data()
loader = IBGEDataLoader()


@app.get("/")
def root():
    return {"message": "Smart Cities API está rodando 🚀 "
                       "Desenvolvido por: Francisco Junior"}


@app.get("/cidades")
def get_cidades(nome: str = None):
    if nome:
        nome_normalizado = normalizar_texto(nome)

        resultado = df[
            df["municipio_normalizado"]
            .str.contains(nome_normalizado)
        ]

        return resultado.to_dict(orient="records")

    return df.to_dict(orient="records")


@app.get("/ranking/pib")
def get_ranking_pib(top_n: int = 10):
    return ranking_pib(df, top_n)


@app.get("/ranking/idhm")
def get_ranking_idhm(top_n: int = 10):
    return ranking_idhm(df, top_n)


@app.get("/ranking/densidade")
def get_ranking_densidade(top_n: int = 10):
    return ranking_densidade(df, top_n)


@app.get("/cidades/{nome}")
def get_cidade(nome: str):
    nome_normalizado = normalizar_texto(nome)

    resultado = df[
        df["municipio_normalizado"]
        .str.contains(nome_normalizado)
    ]

    if resultado.empty:
        raise HTTPException(status_code=404, detail="Cidade não encontrada")

    return resultado.to_dict(orient="records")[0]


@app.get("/ibge/pr/municipios/{id}")
def get_ibge_pr_municipios(id: int):
    # id de maringá: 4115200

    try:
        resultado = loader.get_municipio_por_id(id)
        print(resultado.head())
        print(resultado.columns)

        return resultado.to_dict(orient="records")

    except Exception as e:
        print("ERRO:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ibge/pr/municipios")
def get_ibge_pr_municipios():
    resultado = loader.get_municipios_por_estado("PR")

    return resultado.fillna("").to_dict(orient="records")


@app.get("/maringa/indicadores")
def get_indicadores(
        bairro: str = Query(None),
        zona: str = Query(None)
):
    resultado = df_maringa.copy()

    if bairro:
        resultado = resultado[resultado["bairro"].str.lower() == bairro.lower()]

    if zona:
        resultado = resultado[resultado["zona"].str.lower() == zona.lower()]

    return resultado.to_dict(orient="records")


@app.get("/maringa/indicadores/bairro")
def indicadores_por_bairro():
    resultado = (
        df_maringa.groupby("bairro")[[
            "smart_city_score",
            "indice_qualidade_urbana",
            "indice_infraestrutura_urbana",
            "indice_adensamento_inteligente"
        ]]
        .mean()
        .reset_index()
        .sort_values(by="smart_city_score", ascending=False)
    )

    return resultado.to_dict(orient="records")
