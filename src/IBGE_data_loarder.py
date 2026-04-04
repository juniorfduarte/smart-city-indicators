import requests
import pandas as pd

url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/PR/municipios"

# /api/v1/localidades/estados

# /api/v1/localidades/municipios

# /api/v1/localidades/municipios/{id}

response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)

df["municipio"] = df["nome"]

print(df)