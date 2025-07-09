## 🛠️ Estrutura do Projeto

A organização do projeto segue uma estrutura modular e escalável:

```plaintext
project/
├── .gitignore
├── README.md
├── ChatBot.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── config/ 
│   ├── __init__.py
│   ├── config.py
│   ├── user.json
│   └── utils.py
├── dashboards/
│   ├── __init__.py
│   ├── dashboards_utils.py
│   └── iniciativas_dashboard.py
├── database/
│   ├── __init__.py
│   ├── file_handler.py
│   ├── metadata/
│   │   ├── markdown_indicadores.py
│   │   ├── markdown_padroes.py
│   │   ├── markdown_processor_estrutura.py
│   │   ├── markdown_processor_iniciativas.py
│   │   ├── markdown_processor_oms.py
│   │   ├── markdown_processor_pta.py
│   │   ├── markdown_recursive.py
│   │   └── markdown_riscos.py
│   └── vectorstore_handler.py
├── data/
│   ├── indicadores.csv
│   └── iniciativas.csv
├── documentation/
│   ├── iesgo_structured.md
│   ├── imgg_structured.md
│   ├── Iniciativas.md
│   ├── estatuto_social_structured.md
│   ├── diagnostico_iesgo_structured.md
│   ├── diagnostico_imgg_structured.md
│   ├── indicadores_structured.md
│   ├── instrucoes_chatbot.md
│   ├── oms_unidade.md
│   ├── padroes.md
│   ├── pta_descricao_structured.md
│   ├── riscos_structured.md
│   ├── estrutura_processos_structured.md
│   ├── regimento_interno_structured.md
│   └── instrucoes.md
├── histories/
│   └── checks_confirmed.json
├── memory/
│   ├── __init__.py
│   ├── compaction.py
│   ├── filters.py
│   ├── summarization.py
│   ├── truncation.py
│   └── memory_handler.py
├── pages/
│   ├── 1_📖 Instruções.py
│   ├── 2_⚙️_Editar_Perfil.py
│   ├── 3_📊 Dashboards.py
│   └── 4_👑_Admin.py
├── pipeline/
│   ├── __init__.py
│   ├── handler.py
│   ├── stream.py
│   └── utils.py
├── prompt/
│   ├── __init__.py
│   └── prompt_template.py
├── retriever/
│   ├── __init__.py
│   ├── retrievers.py
│   └── section.py
```

# API de IA com FastAPI utilizando Gemini LLM

Este projeto é uma API desenvolvida em Python utilizando o framework **FastAPI** integrada à LLM do Gemini, facilitando a criação de aplicações de Inteligência Artificial de maneira simples, performática e escalável.

## Sumário

- [Descrição](#descrição)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Rodar a API](#como-rodar-a-api)
- [Como acessar a documentação (Swagger)](#como-acessar-a-documentação-swagger)
- [Sobre o FastAPI e Uvicorn](#sobre-o-fastapi-e-uvicorn)

---

## Descrição

Esta API expõe endpoints para interação com modelos de linguagem natural do Gemini, utilizando a robustez do **FastAPI** e diversas bibliotecas para manipulação e orquestração dos modelos. Ideal para aplicações que necessitam de processamento de linguagem natural, chatbots, assistentes virtuais, análise de texto, entre outros.

---

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para criação de APIs em Python.
- **Uvicorn**: Servidor ASGI leve e de alta performance, utilizado para rodar aplicações FastAPI.
- **google-genai** & **langchain**: Bibliotecas para integração com LLMs, especialmente Gemini.
- **pydantic**: Validação de dados e criação de schemas.
- **orjson**: Serialização/deserialização de JSON extremamente rápida.
- **faiss-cpu**: Busca vetorial de alta performance.
- Outras: `requests`, `python-dotenv`, `tiktoken`, `python-multipart`, `google-auth`, `google-api-core`.

---

## Requisitos

- Python 3.9 ou superior
- Git (opcional para clonar o repositório)

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto e adicione as credenciais necessárias para o acesso à API do Gemini e demais serviços do Google. Por exemplo:

```
GOOGLE_API_KEY="API_KEY_GERADA"
```

---

## Como Rodar a API

Após instalar as dependências e configurar o `.env`, execute:

```bash
uvicorn main_api:app --host 0.0.0.0 --port 8001 --reload
```

Por padrão, a API estará disponível em [http://127.0.0.1:8001](http://127.0.0.1:8001).

---

## Como acessar a documentação (Swagger)

O FastAPI fornece uma interface interativa de documentação e teste dos endpoints (Swagger UI).

Acesse:

- [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs) – Swagger UI
- [http://127.0.0.1:8001/redoc](http://127.0.0.1:8001/redoc) – ReDoc

---

## Sobre o FastAPI e o Uvicorn

- **FastAPI**:
  - Framework moderno, rápido (alta performance), fácil de usar e robusto para criação de APIs RESTful.
  - Utiliza tipagem do Python para validação de dados automática via Pydantic.
  - Gera documentação automática dos endpoints.

- **Uvicorn**:
  - Servidor ASGI de alta performance, recomendado para rodar aplicações FastAPI em produção ou desenvolvimento.
  - Suporta recursos assíncronos (async/await), ideal para aplicações modernas e escaláveis.

---

## Produção

Para rodar em produção, recomenda-se executar o Uvicorn com um servidor como Gunicorn:

```bash
gunicorn -k uvicorn.workers.UvicornWorker main_api:app --host 0.0.0.0 --port 8001
```

---

## Suporte

Em caso de dúvidas entre em contato comigo por E-mail:
+ matheusloboo2001@gmail.com

---