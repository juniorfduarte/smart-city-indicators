from fastapi import FastAPI
from src.data_loader import load_data, normalizar_texto
from src.indicators import ranking_pib, ranking_idhm, ranking_densidade
from fastapi import HTTPException

app = FastAPI()

df = load_data()


@app.get("/")
def root():
    return {"message": "Smart Cities API está rodando 🚀 \n Desenvolvido por: Francisco Junior"}


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
