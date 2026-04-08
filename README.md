# 🏙️ Smart City Indicators

API para análise e exposição de indicadores urbanos a partir de dados públicos (IBGE), com foco em **Smart Cities**.

---

## 🎯 Objetivo

Este projeto tem como objetivo:

* Consumir dados abertos de cidades brasileiras
* Processar e gerar indicadores urbanos relevantes
* Disponibilizar os dados através de uma API REST
* Evoluir para um serviço público com deploy em nuvem

---

## 📊 Indicadores (MVP)

Atualmente, o projeto trabalha com:

* Densidade demográfica
* PIB per capita
* IDHM (Índice de Desenvolvimento Humano Municipal)

---

## 🧱 Tecnologias utilizadas

* Python
* Pandas
* FastAPI
* Uvicorn

---

## 📁 Estrutura do projeto

```
smart-city-indicators/
│
├── data/                  # Arquivos de dados (IBGE)
├── src/
│   ├── api.py             # Definição da API (FastAPI)
│   ├── data_loader.py     # Ingestão e limpeza dos dados
│   ├── indicators.py      # Regras de negócio (indicadores)
│   └── main.py            # Testes locais
│
└── requirements.txt
```

---

## 🚀 Como executar o projeto

### 1. Atualizar os requirements.txt

```
pip freeze > requirements.txt
```

---

### 2. Crie um ambiente virtual (recomendado)

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Instale as dependências

```
pip install -r requirements.txt
```

---

### 4. Execute a API

```
uvicorn src.api:app --reload
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

## 🧪 Status do projeto

🚧 Em desenvolvimento (MVP em construção)

---

## 🔜 Próximos passos

* [ ] Criar endpoints de ranking (PIB, IDHM, densidade)
* [ ] Adicionar persistência com banco de dados
* [ ] Criar dashboard de visualização
* [ ] Realizar deploy em nuvem

---

## 📌 Observações

* Os dados utilizados são provenientes de fontes públicas (IBGE)
* O projeto segue uma abordagem incremental, evoluindo de um MVP simples para um serviço completo

---

## 👨‍💻 Autor

Desenvolvido por Francisco Ferreira Duarte Junior, como projeto de estudo e prática em engenharia de software e dados.
