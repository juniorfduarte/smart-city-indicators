# Smart City Indicators — contexto do projeto

Projeto de doutorado + portfólio: indicadores de smart city para Maringá-PR. Repositório público, sem dados sensíveis expostos.

## Setup local

- Python 3.11 (pinado em `.python-version`). Venv já existe em `venv/` na raiz — **não recriar**.
  - Ativar: `source venv/bin/activate`, ou usar direto `venv/bin/python`, `venv/bin/pytest`.
  - Instalar deps: `venv/bin/pip install -r requirements.txt -r requirements-dev.txt`
- Rodar testes: `venv/bin/pytest` (ou `pytest` com o venv ativado).
- Frontend (`frontend/`): React + Vite, único frontend a manter (Streamlit em `dashboard/` está planejado para remoção, ver Track B §12).

## Estrutura: dois tracks, sem imports cruzados

- **Track A — Municipal/Prefeitura** (existente, dados mockados): `src/maringa_data_loader.py`, rotas `/maringa/*`, `/cidades`, `/ranking/*`, `/ibge/pr/*`. Mantido como está.
- **Track B — Dados Abertos / IUA** (`src/censo_urbano/`): linha paralela baseada em dados abertos do Censo 2022 (IBGE), independente da prefeitura. Índice **IUA — Índice Urbano Aberto**, inspirado na metodologia do IBEU (Observatório das Metrópoles), não é implementação oficial dela.

## Track B — spec-driven, fonte de verdade em doc privado

O spec completo (metodologia, regras de cálculo, decisões, checklist por fase) é mantido
num workspace privado fora deste repositório — não linkado aqui por ser um repo público.
O link fica salvo na memória local do Claude Code para este projeto; se precisar dele e
não estiver disponível, pergunte ao usuário.

**Fluxo de trabalho combinado com o usuário:** o Claude executa as tasks (código, testes), mas commit e push ficam **sempre** por conta do usuário — nunca rodar `git commit`/`git push` neste track sem pedido explícito.

### Status (atualizado 2026-07-16)

- ✅ Fase 1 (domain — cálculo puro) e Fase 2 (repositories — I/O real) implementadas, testadas e mergeadas em `master`.
- Dados reais do Censo 2022 baixados em `data/raw/censo2022/` (gitignored, ~228MB) + recorte filtrado para Maringá em `data/raw/censo2022/maringa/` (~3MB, `CD_MUN=4115200`, 793 setores).
- `geopandas==1.1.4` no requirements.txt (só para `malha_repository.py`).
- Suíte completa: 73 testes passando.
- **Próximo passo: Fase 3** — `schemas/setor.py` (Pydantic), `services/iua_service.py`, `api/router.py`.
- **Decisão pendente para a Fase 3:** o Censo usa `"X"` como marcador de sigilo estatístico em células individuais (não só em setores sem domicílios). Indicadores que somam múltiplas variáveis (água = 8 variáveis, espécie = 3) precisam decidir como tratar uma célula suprimida dentro da soma — provável: tratar como 0 (`skipna=True`), documentando como desvio consciente. Ver addendum na página "Spec" do Notion (2026-07-16) para os 25 setores reais afetados.

## Padrões de código já estabelecidos

- Pandas-first, funções puras separadas de I/O (ver `src/censo_urbano/domain/` vs `repositories/`).
- Testes com `pytest`, classes `TestNomeDaFuncao`, fixtures pequenas/sintéticas (não o dataset real nos testes).
- API: `TestClient` + `app.dependency_overrides` (ver `tests/conftest.py`).
