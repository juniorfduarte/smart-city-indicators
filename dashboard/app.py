import streamlit as st
import pandas as pd
import requests

# API_URL = "http://127.0.0.1:8000/maringa/indicadores"
API_URL = "https://smart-city-indicators.onrender.com/maringa/indicadores"

st.set_page_config(page_title="Smart City Dashboard", layout="wide")

st.title("🏙️ Smart City Dashboard - Maringá")

# ------------------------
# Filtros
# ------------------------

bairro = st.text_input("Filtrar por bairro")
zona = st.text_input("Filtrar por zona")

params = {}
if bairro:
    params["bairro"] = bairro

if zona:
    params["zona"] = zona

# ------------------------
# Carregar dados
# ------------------------

response = requests.get(API_URL, params=params)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    if df.empty:
        st.warning("Nenhum dado encontrado.")
    else:
        # ------------------------
        # KPIs
        # ------------------------
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Score Médio",
            round(df["smart_city_score"].mean(), 3)
        )

        col2.metric(
            "Infraestrutura Média",
            round(df["indice_infraestrutura_urbana"].mean(), 3)
        )

        col3.metric(
            "Qualidade Urbana",
            round(df["indice_qualidade_urbana"].mean(), 3)
        )

        # ------------------------
        # Ranking
        # ------------------------
        st.subheader("🏆 Top Lotes")

        df_sorted = df.sort_values(by="smart_city_score", ascending=False)

        st.dataframe(
            df_sorted[
                [
                    "id_lote",
                    "bairro",
                    "zona",
                    "smart_city_score",
                    "indice_qualidade_urbana"
                ]
            ].head(20)
        )

        # ------------------------
        # Gráfico por bairro
        # ------------------------
        st.subheader("📊 Score médio por bairro")

        df_bairro = (
            df.groupby("bairro")["smart_city_score"]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(df_bairro)

        # ------------------------
        # Distribuição
        # ------------------------
        st.subheader("📈 Distribuição do Score")

        st.line_chart(df["smart_city_score"])

        # ------------------------
        # Dados brutos
        # ------------------------
        with st.expander("🔍 Ver dados completos"):
            st.dataframe(df)

else:
    st.error("Erro ao conectar com a API")