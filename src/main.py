from data_loader import load_data
from indicators import ranking_pib


def space():
    print("------------------------------------------------------------------------------")


df = load_data()

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
