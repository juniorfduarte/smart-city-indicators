"""Constantes do Índice Urbano Aberto (IUA) — Track B, dados abertos (Censo 2022).

Unidade dos indicadores: DOMICÍLIOS (decisão de 2026-07-15, resolve a
divergência entre §6.2 e §10 do spec "Índice Urbano v1").
"""

UNIVERSO_PADRAO = "maringa"

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

# casa, casa de vila/condomínio, apartamento = adequado;
# cômodos/cortiço, habitação indígena, estrutura degradada = inadequado.
# Inferência a partir da descrição oficial (ordem V00047→V00052), consistente com a
# distinção "convencional vs. inadequado" da metodologia original do IBEU — CONFIRMAR
# contra o Dicionário oficial antes da Fase 2 (repositories).
ESPECIE_ADEQUADA_V00XXX = ["V00047", "V00048", "V00049"]
ESPECIE_TOTAL_V00XXX = [f"V00{n}" for n in range(47, 53)]

# Faixas de banheiro (domicílios) e moradores por faixa: ranges confirmados no spec,
# mas a ordem faixa→código dentro do range NÃO está confirmada — mapear contra o
# Dicionário oficial do Censo 2022 na Fase 2 (repositories), não inventar aqui.
BANHEIRO_DOMICILIOS_V00XXX_RANGE = [f"V00{n}" for n in range(232, 239)]
BANHEIRO_MORADORES_V00XXX_RANGE = [f"V00{n}" for n in range(552, 559)]

# §6.3: piso conservador de nº de banheiros para a faixa "4+"
PISO_BANHEIROS_FAIXA_4_MAIS = 4

# §6.3: limiar de densidade morador/banheiro considerada adequada (<=)
LIMIAR_DENSIDADE_BANHEIRO = 4
