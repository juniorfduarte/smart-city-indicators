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

### Status (atualizado 2026-07-21)

- ✅ Fase 1 (domain — cálculo puro), Fase 2 (repositories — I/O real) e Fase 3 (schemas/service/router) implementadas e testadas. Commit/push ainda não feitos (por conta do usuário).
- Dados reais do Censo 2022 baixados em `data/raw/censo2022/` (gitignored, ~228MB) + recorte filtrado para Maringá em `data/raw/censo2022/maringa/` (~3MB, `CD_MUN=4115200`, 793 setores).
- `geopandas==1.1.4` no requirements.txt (só para `malha_repository.py`).
- Suíte completa: 86 testes passando.
- **Fase 3 implementada e revisada (code review multi-agente):** `schemas/setor.py` (`SetorIUA`), `services/iua_service.py` (`calcular_iua_setores(df_setores)` — orquestra repositories + domain, trata sigilo em soma como 0 e "não aglomerado subnormal" via `CD_FCU`, que vem do arquivo básico já dentro de `df_setores`), `api/router.py` (`GET /iua/setores`, `GET /iua/setores/{cd_setor}`, via `APIRouter` isolado). **Validado ponta a ponta contra os 793 setores reais de Maringá** (32 sem_dado, IUA médio ~0.9566).
- **Router montado no app principal (2026-07-17):** `src/api.py` agora importa `iua_router` e faz `include_router`; `load_setores_iua()` (carrega + calcula via `censo_repository.carregar_setores` + `iua_service.calcular_iua_setores`, caminhos reais em `censo_urbano/config.py`) roda no `lifespan` e popula `app.state.setores_iua`, que a dependência `get_setores_iua` do router já lia. `tests/conftest.py` atualizado para mockar `src.api.load_setores_iua` e sobrescrever `get_setores_iua`, igual ao padrão dos outros loaders — suíte geral não bate no Censo real. Smoke test end-to-end com lifespan real confere os 793 setores/32 sem_dado/IUA médio, e as rotas do Track A (`/health`, `/cidades`) continuam OK.
- **Decisão confirmada (sigilo estatístico), com fonte oficial:** célula `"X"` é tratada como 0 (`fillna(0)`), aplicado uniformemente a todos os indicadores (não só somas multivariáveis). Confirmado contra o PDF oficial do IBGE ("Agregados por Setores Censitários: Resultados do universo", slide 13, "Tratamento de sigilo"): a supressão só ocorre quando o **valor da própria célula** é 1 ou 2 ("deve ser evitada a divulgação de células com frequências iguais a 1 ou 2") — nunca por causa do complemento/total. Ou seja, "X" sempre significa "valor pequeno" (1 ou 2), então tratar como 0 introduz um erro máximo de 1-2 domicílios por célula, aceitável em qualquer setor não-sem_dado.
- **Limiar de `sem_dado` corrigido para bater com a metodologia oficial do IBGE:** o mesmo PDF (slide 13) diz que setores com **menos de 5 domicílios particulares permanentes** têm a maioria das variáveis omitida (só ficam identificação geográfica, número de domicílios e população). `calcular_sem_dado` (domain/index.py) mudou de `total_domicilios == 0` para `total_domicilios < 5`. Também adicionada uma máscara explícita de `sem_dado` sobre d3/d4/iua em `iua_service.py`, porque esgoto/lixo/densidade de banheiro usam o total de domicílios externo (sempre > 0 para 1-4 domicílios) como denominador e não ficavam NaN sozinhos por propagação — só água/espécie (que têm denominador somado internamente) ficavam NaN "por acaso". Validado contra os 793 setores reais: sem_dado subiu de 22 (limiar antigo) para 32 (limiar novo), estatísticas de IUA idênticas (confirma que os 10 setores adicionais já estavam silenciosamente NaN).
- **Bugs corrigidos na revisão (pré-existentes, Fase 1/2, expostos agora porque Fase 3 é o primeiro consumidor real):**
  - `ESPECIE_TOTAL_V00XXX` em `config.py` gerava códigos errados (`V0047` em vez de `V00047`).
  - `TOTAL_DOMICILIOS_V0007` apontava para uma coluna inexistente (`"V0007"`) — a coluna real do arquivo básico é `"v0007"` minúsculo.
  - `malha_repository.carregar_malha_setores` esperava `CD_MUN`/`SITUACAO`/`CD_FCU` no `.gpkg`, mas o arquivo real de Maringá só tem `CD_SETOR` + `geometry`. Corrigido simplificando a malha para só geometria (o `CD_FCU` já vem do arquivo básico, via `df_setores`) — `calcular_iua_setores` não recebe mais `df_malha`.
- **Página de documentação do IUA no frontend concluída (2026-07-21):** `frontend/src/pages/IUADocumentacao.jsx` (metodologia, fontes, limitações — mesmo padrão de `Indicadores.jsx`), registrada em `Sidebar.jsx`/`App.jsx`. Conferida no navegador via script Playwright (`frontend/screenshot_iua_doc.mjs`, não faz parte do build, só ferramenta de conferência ad-hoc).
- **Mapa interativo do IUA no frontend (2026-07-21):** novo endpoint `GET /iua/setores/geojson` (`src/api.py`: `load_setores_iua_geojson` no `lifespan`, popula `app.state.setores_iua_geojson`; `src/censo_urbano/api/router.py` expõe a rota) — junta a malha real (`malha_repository.carregar_malha_setores`, reprojetada de EPSG:4674 para 4326) com o IUA/D3/D4 já calculados, retornando um `FeatureCollection` GeoJSON. Frontend (`frontend/src/pages/IUA.jsx`) ganhou um mapa Leaflet (`react-leaflet` + `leaflet`, novas deps) com choropleth dos 793 setores, posicionado acima do histograma "Distribuição do IUA". Os 4 KPI cards (IUA médio, D3, D4, Setores sem dado) viram um seletor/filtro do mapa: clique ativa (recolore o mapa pelo indicador daquele card, ou isola os setores sem dado em destaque); clicar de novo desativa e volta ao padrão. **Padrão = nenhum card ativo, todos os 793 setores exibidos, colorido por IUA.** Rampas de cor sequenciais (uma por indicador: indigo/verde/âmbar) validadas com a skill de dataviz (`validate_palette.js --ordinal`). `tests/conftest.py` mocka o novo endpoint (`MOCK_SETORES_IUA_GEOJSON`) seguindo o padrão já estabelecido.
- **Pendente:** próxima fase do spec (se houver) — Fases 1-4 (frontend incluído) concluídas. Remover `dashboard/` (Streamlit) e `requirements-dashboard.txt` segue pendente (ver README também desatualizado).

## Padrões de código já estabelecidos

- Pandas-first, funções puras separadas de I/O (ver `src/censo_urbano/domain/` vs `repositories/`).
- Testes com `pytest`, classes `TestNomeDaFuncao`, fixtures pequenas/sintéticas (não o dataset real nos testes).
- API: `TestClient` + `app.dependency_overrides` (ver `tests/conftest.py`).
