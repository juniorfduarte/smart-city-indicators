"""Constantes do Índice Urbano Aberto (IUA) — Track B, dados abertos (Censo 2022).

Unidade dos indicadores: DOMICÍLIOS (decisão de 2026-07-15, resolve a
divergência entre §6.2 e §10 do spec "Índice Urbano v1").
"""

UNIVERSO_PADRAO = "maringa"

# Confirmado em 2026-07-16 diretamente nos dados oficiais (coluna CD_MUN)
CD_MUN_MARINGA = "4115200"

# Denominador genérico de "total de domicílios do setor" (esgoto, lixo): decisão de
# 2026-07-16 — Domicílios Particulares Ocupados, exclui vagos/uso ocasional (sem
# morador para ter condição de esgoto/lixo avaliada).
TOTAL_DOMICILIOS_V0007 = "V0007"

# --- Pesos por dimensão (redistribuídos — indicadores N/A no Censo 2022 excluídos) ---

# D4 Serviços Coletivos: pesos originais água=1/5, esgoto=2/5, lixo=1/5, energia=1/5 (N/A).
# Energia elétrica não existe como variável no Censo 2022 — peso redistribuído
# proporcionalmente (×5/4) entre os 3 indicadores restantes.
PESO_AGUA_D4 = 0.25
PESO_ESGOTO_D4 = 0.5
PESO_LIXO_D4 = 0.25

# D3 Condições Habitacionais: pesos originais de 5 indicadores (1/5 cada).
# Parede adequada e densidade morador/dormitório não existem no Censo 2022 —
# peso redistribuído igualmente entre os 3 indicadores restantes.
PESO_NAO_AGLOMERADO_SUBNORMAL_D3 = 1 / 3
PESO_DENSIDADE_BANHEIRO_D3 = 1 / 3
PESO_ESPECIE_ADEQUADA_D3 = 1 / 3

# --- Códigos de variáveis (Dicionário Censo 2022 — Agregados por Setor, Resultados do Universo) ---
# Confirmados em §6.1 do spec. NÃO usar códigos de 2010.

AGUA_ADEQUADA_V00XXX = ["V00111"]  # rede geral de distribuição
AGUA_TOTAL_V00XXX = [f"V00{n}" for n in range(111, 119)]  # todas as formas de abastecimento

ESGOTO_ADEQUADO_V00XXX = ["V00309"]  # rede geral ou pluvial

LIXO_ADEQUADO_V00XXX = ["V00397", "V00398"]  # coletado por serviço de limpeza + depositado em caçamba

# casa, casa de vila/condomínio, apartamento = adequado (V00047-049);
# cômodos/cortiço, habitação indígena, estrutura degradada = inadequado (V00050-052).
# Confirmado em 2026-07-16 contra o Dicionário oficial (descrições exatas por variável).
ESPECIE_ADEQUADA_V00XXX = ["V00047", "V00048", "V00049"]
ESPECIE_TOTAL_V00XXX = [f"V00{n}" for n in range(47, 53)]

# Faixas de banheiro: domicílios em domicilio2 (V00232-238), moradores em domicilio3
# (V00552-558) — mesma ordem em ambos os arquivos, confirmado em 2026-07-16 contra o
# Dicionário oficial: 1, 2, 3, 4+, comum, sanitário/buraco, nenhum.
FAIXAS_BANHEIRO = [
    {"nome": "1_banheiro", "num_banheiros": 1, "domicilios_v00xxx": "V00232", "moradores_v00xxx": "V00552"},
    {"nome": "2_banheiros", "num_banheiros": 2, "domicilios_v00xxx": "V00233", "moradores_v00xxx": "V00553"},
    {"nome": "3_banheiros", "num_banheiros": 3, "domicilios_v00xxx": "V00234", "moradores_v00xxx": "V00554"},
    {"nome": "4_mais_banheiros", "num_banheiros": 4, "domicilios_v00xxx": "V00235", "moradores_v00xxx": "V00555"},
    {"nome": "comum", "num_banheiros": None, "domicilios_v00xxx": "V00236", "moradores_v00xxx": "V00556"},
    {"nome": "sanitario_buraco", "num_banheiros": None, "domicilios_v00xxx": "V00237", "moradores_v00xxx": "V00557"},
    {"nome": "nenhum", "num_banheiros": None, "domicilios_v00xxx": "V00238", "moradores_v00xxx": "V00558"},
]

# §6.3: piso conservador de nº de banheiros para a faixa "4+"
PISO_BANHEIROS_FAIXA_4_MAIS = 4

# §6.3: limiar de densidade morador/banheiro considerada adequada (<=)
LIMIAR_DENSIDADE_BANHEIRO = 4
