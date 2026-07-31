# 🏙️ Smart City Indicators

API para análise e exposição de indicadores urbanos a partir de dados públicos (IBGE) e dados da prefeitura de Maringá-PR, com foco em **Smart Cities**.

Projeto de doutorado + portfólio, organizado em duas linhas independentes:

* **Track A — Municipal/Prefeitura**: indicadores com dados mockados da prefeitura de Maringá (rotas `/maringa/*`, `/cidades`, `/ranking/*`, `/ibge/pr/*`).
* **Track B — Dados Abertos / IUA**: índice **IUA — Índice Urbano Aberto**, calculado a partir de dados abertos do Censo 2022 (IBGE), inspirado na metodologia do IBEU (Observatório das Metrópoles) — não é uma implementação oficial dela (rotas `/iua/*`).

---

## 🎯 Objetivo

Este projeto tem como objetivo:

* Consumir dados abertos de cidades brasileiras (IBGE) e dados mockados da prefeitura de Maringá
* Processar e gerar indicadores urbanos relevantes
* Disponibilizar os dados através de uma API REST (FastAPI)
* Oferecer um frontend em React para visualização dos indicadores e do mapa interativo do IUA
* Evoluir para um serviço público com deploy em nuvem

---

## 📊 Indicadores

**Track A (mockados):**

* Densidade demográfica
* PIB per capita
* IDHM (Índice de Desenvolvimento Humano Municipal)

**Track B — IUA (dados reais, Censo 2022):**

* IUA geral por setor censitário de Maringá, mais os sub-indicadores D3 (esgoto/lixo/banheiro) e D4 (densidade/aglomerado subnormal)
* Mapa interativo (choropleth) e documentação da metodologia no frontend

---

## 🧱 Tecnologias utilizadas

* Python 3.11 / Pandas / FastAPI / Uvicorn
* Geopandas (malha de setores censitários)
* React + Vite (frontend), Leaflet (mapa do IUA), Recharts (gráficos)
* Docker

---

## 📁 Estrutura do projeto

```
smart-city-indicators/
│
├── src/
│   ├── api.py                # API principal (FastAPI) — Track A + monta o router do Track B
│   ├── data_loader.py         # Ingestão e limpeza (Track A, mock)
│   ├── ibge_data_loader.py
│   ├── maringa_data_loader.py
│   ├── indicators.py          # Regras de negócio (Track A)
│   └── censo_urbano/          # Track B — IUA
│       ├── domain/            # regras de cálculo puras (IUA, D3, D4)
│       ├── repositories/      # leitura dos dados do Censo/malha (I/O)
│       ├── schemas/
│       ├── services/          # orquestração (domain + repositories)
│       ├── api/                # router isolado (/iua/*)
│       └── config.py
│
├── frontend/                  # React + Vite — único frontend mantido
│   └── src/pages/
│       ├── Dashboard.jsx
│       ├── Indicadores.jsx
│       ├── IUA.jsx            # mapa interativo + KPIs do IUA
│       └── IUADocumentacao.jsx
│
├── data/                       # dados mockados (Track A) e recorte do Censo 2022 (Track B, gitignored)
├── tests/                      # pytest (unit + API via TestClient)
│
├── Dockerfile.api
├── docker-compose.yml
├── requirements.txt
└── README.md
```

> `dashboard/` (Streamlit) e `requirements-dashboard.txt` ainda existem no repositório mas estão **descontinuados** — pendente de remoção.

---

# 🚀 Como executar o projeto

### 🥇 Opção 1 — API via Docker + Frontend local (Recomendado)

Pré-requisitos: Docker e Docker Compose instalados.

1. Subir a API
```
docker-compose up --build api
```

2. Rodar o frontend (em outro terminal)
```
cd frontend
npm install
npm run dev
```

3. Acessar a aplicação
   1. Frontend (React/Vite): http://localhost:5173
   2. API: http://localhost:8000
   3. Documentação (Swagger): http://localhost:8000/docs

- O serviço `api` do `docker-compose.yml` tem hot reload automático — alterações em `.py` são refletidas sem rebuild.
- Execute novamente com `--build` apenas se alterar `requirements.txt`, `Dockerfile.api` ou adicionar novas dependências Python.
- O serviço `frontend` do `docker-compose.yml` ainda sobe o dashboard Streamlit legado — ignore-o (será removido).

---

### 🥈 Opção 2 — Rodar tudo localmente (sem Docker)

Requer Python 3.11 (versão pinada em `.python-version`) e Node.js.

1. Criar ambiente virtual e instalar dependências Python
```
python3.11 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt   # opcional, para rodar testes/lint
```

2. Rodar a API
```
uvicorn src.api:app --reload
```

3. Rodar o frontend
```
cd frontend
npm install
npm run dev
```

4. Rodar os testes
```
pytest
```

---

## 🌐 Acessando a aplicação

### Produção (Render)

* Frontend: https://smart-city-indicators-frontend.onrender.com
* API: https://smart-city-indicators.onrender.com
* Swagger: https://smart-city-indicators.onrender.com/docs
* Status page: https://stats.uptimerobot.com/2DFhGENYiE

🔥 A documentação da API é gerada automaticamente pelo FastAPI.

### Local

* Frontend: http://localhost:5173
* API: http://127.0.0.1:8000
* Swagger: http://127.0.0.1:8000/docs

---

## 🧪 Status do projeto

🚧 Em desenvolvimento

* ✅ Track A (mockado) e Track B/IUA (dados reais do Censo 2022 para Maringá) implementados, testados e em produção.
* ✅ Frontend React com dashboard, indicadores, documentação e mapa interativo do IUA.
* 🔜 Remoção do dashboard Streamlit legado (`dashboard/`, `requirements-dashboard.txt`).

---

## 📌 Observações

* Os dados da Track A (indicadores da prefeitura de Maringá) são totalmente fictícios/mockados.
* Os dados da Track B (IUA) são reais, provenientes do Censo 2022 (IBGE) — Agregados por Setores Censitários.
* O IUA é um índice próprio deste projeto, inspirado na metodologia do IBEU (Observatório das Metrópoles), e não constitui uma implementação oficial dela.
* O projeto segue uma abordagem incremental, evoluindo de um MVP simples para um serviço completo.

---

## 👨‍💻 Autor

Desenvolvido por Francisco Ferreira Duarte Junior, como projeto de estudo e prática em engenharia de software e dados.
