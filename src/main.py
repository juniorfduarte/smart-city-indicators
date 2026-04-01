from data_loader import load_data
from indicators import ranking_pib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dados_ibge_pr.xlsx"


def space():
    print("------------------------------------------------------------------------------")


df = load_data(DATA_PATH.__str__())

# print(df.head())
# space()
#
# print(df.describe())
# space()
#
# df.columns = df.columns.str.strip()
# print(df.describe())
# space()
#
# df.columns = df.columns.str.lower()
# print(df.describe())
# space()
#
# print(df.columns.tolist())
# space()

maringa = df[df['municipio'] == 'Maringá']
print(maringa)
space()

pib = ranking_pib(df)
print("Ranking 10 maiores PIBs:")
print(pib[:3])
space()
