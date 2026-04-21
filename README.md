# 🏙️ Smart City Indicators

API para análise e exposição de indicadores urbanos a partir de dados públicos (IBGE) e dados da prefeitura de Maringá-PR, com foco em **Smart Cities**.

---

## 🎯 Objetivo

Este projeto tem como objetivo:

* Consumir dados abertos de cidades brasileiras
* Processar e gerar indicadores urbanos relevantes
* Disponibilizar os dados através de uma API REST
* Oferecer um dashboard interativo para visualização
* Evoluir para um serviço público com deploy em nuvem

---

## 📊 Indicadores (MVP)

Atualmente, o projeto trabalha com:

* Densidade demográfica
* PIB per capita
* IDHM (Índice de Desenvolvimento Humano Municipal)
* TODO => Criar sub-pages sobre os indicadores

---

## 🧱 Tecnologias utilizadas

* Python
* Pandas
* FastAPI
* Uvicorn
* Streamlit 
* Docker

---

## 📁 Estrutura do projeto

```
smart-city-indicators/ 
│ 
├── dashboard/ 
│ 
├── app.py # Front-end (Streamlit) 
├── data/ # Dados mockados (IBGE) 
├── src/ 
│ 
├── api.py # API (FastAPI) 
│ 
├── data_loader.py # Ingestão e limpeza 
│ 
├── indicators.py # Regras de negócio 
│ 
└── main.py # Testes locais 
│ 
├── Dockerfile.api 
├── Dockerfile.frontend 
├── docker-compose.yml 
├── requirements.txt 
└── README.md
```

---

# 🚀 Como executar o projeto


### 🥇 Opção 1 — Rodar com Docker (Recomendado)

### Pré-requisitos

- Docker instalado

- Docker Compose instalado

### Subindo a aplicação:

1. Subir toda a aplicação

```
docker-compose up --build
```

2. Acessar a aplicação

   1. Frontend (Streamlit):
   http://localhost:8501

   2. API:
   http://localhost:8000

   3. Documentação (Swagger):
   http://localhost:8000/docs


- O projeto está configurado com hot reload automático:

- Alterações no código são refletidas automaticamente
Não é necessário rebuild para mudanças em .py


### Quando usar --build novamente

Execute novamente com --build apenas se:

- Alterar requirements.txt
- Alterar Dockerfile
- Adicionar novas dependências
---

### 🥈 Opção 2 — Rodar localmente (sem Docker)

1. Criar ambiente virtual
```
python -m venv venv
venv\Scripts\activate   # Windows
```
2. Instalar dependências
```
pip install -r requirements.txt
```
3. Rodar API
```
uvicorn src.api:app --reload
```

4. Rodar Frontend:
```
streamlit run dashboard/app.py
```

---

## 🌐 Acessando a aplicação

### Aplicação em Produção:
A aplicação está hospetada e acessível nos links abaixo:

* URL base:
  https://smart-city-indicators.onrender.com
* URL de endpoints/docs:
  https://smart-city-indicators.onrender.com/docs

### Rodando Localmente:
Após iniciar o servidor, acesse:

* API:
  http://127.0.0.1:8000

* Documentação interativa (Swagger):
  http://127.0.0.1:8000/docs

🔥 A documentação é gerada automaticamente pelo FastAPI.

---
### Produção (Render)
* Frontend: https://smart-city-indicators-frontend.onrender.com

* API: https://smart-city-indicators.onrender.com

* Swagger: https://smart-city-indicators.onrender.com/docs

* Status page: https://stats.uptimerobot.com/2DFhGENYiE



### Local
* Frontend: http://localhost:8501

* API: http://127.0.0.1:8000

* Swagger: http://127.0.0.1:8000/docs

---

## 🧪 Status do projeto

🚧 Em desenvolvimento (MVP em construção)

---

## 📌 Observações

* Os dados referentes à cidade de Maringá são totalmente fictícios
* Demais dados são provenientes de fontes públicas (IBGE)
* O projeto segue uma abordagem incremental, evoluindo de um MVP simples para um serviço completo

---

## 👨‍💻 Autor

Desenvolvido por Francisco Ferreira Duarte Junior, como projeto de estudo e prática em engenharia de software e dados.
