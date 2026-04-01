from fastapi import FastAPI
from src.data_loader import load_data
from src.indicators import ranking_pib, ranking_idhm, ranking_densidade

app = FastAPI()

df = load_data()


@app.get("/")
def root():
    return {"message": "Smart Cities API está rodando 🚀 \n Desenvolvido por: Francisco Junior" }


@app.get("/cidades")
def get_cidades():
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