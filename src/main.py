from data_loader import load_data
from indicators import ranking_pib
from src.utils import space

# Origem dos dados: https://www.ibge.gov.br/cidades-e-estados/pr/maringa.html


df = load_data()

maringa = df[df['municipio'] == 'Maringá']
print(maringa)
space()

pib = ranking_pib(df)
print("Ranking 10 maiores PIBs:")
print(pib[:3])
space()
