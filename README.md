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

Estrutura de Projeto Profissional para API de IA
Esta estrutura organiza o projeto em camadas lógicas (API, Lógica de Negócio, Acesso a Dados), tornando-o escalável, testável e fácil de manter.

Visão Geral da Arquitetura
api/: Contém toda a lógica da API web (FastAPI).

routers/: Define os endpoints, agrupados por funcionalidade (usuários, documentos, etc.). É a porta de entrada para as requisições.

schemas/: Contém os modelos Pydantic, que definem a "forma" dos dados que entram e saem da API, garantindo validação e documentação automática.

crud/: Camada de "Create, Read, Update, Delete". Abstrai a lógica de manipulação dos dados, seja de um banco de dados de usuários ou de arquivos de configuração.

dependencies.py: Gerencia a injeção de dependências, como obter o usuário logado ou uma instância de um pipeline.

main.py: Ponto de entrada que monta a aplicação FastAPI, incluindo os routers e middlewares.

database/: Responsável pela interação com os dados brutos e os vectorstores.

metadata_split/: Contém seus scripts customizados para processar cada tipo de documento.

ingestion.py: Orquestra o processo de reindexação, usando seus scripts customizados.

vectorstore_handler.py: Abstrai a criação e o carregamento dos vectorstores FAISS.

retriever/ e pipeline/: Contêm a lógica principal da sua IA, agora configurável dinamicamente através de arquivos JSON gerenciados pela API.

Arquivos de Configuração (.json): Armazenam os parâmetros dos retrievers e pipelines, permitindo alterações em tempo real via API sem a necessidade de reiniciar o servidor.

Estrutura de Diretórios Final
.
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── security.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user_crud.py
│   │   ├── retriever_crud.py
│   │   └── pipeline_crud.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── documents.py
│   │   ├── users.py
│   │   ├── retrievers.py
│   │   ├── pipelines.py
│   │   └── system.py
│   └── schemas/
│       ├── __init__.py
│       ├── chat.py
│       ├── document.py
│       ├── user.py
│       ├── retriever.py
│       ├── pipeline.py
│       └── system.py
├── database/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── vectorstore_handler.py
│   └── metadata_split/
│       ├── markdown_gerente.py
│       ├── markdown_indicadores.py
│       └── ... (todos os seus outros processadores)
├── pipeline/
│   ├── __init__.py
│   ├── config_manager.py
│   ├── handler.py
│   └── utils.py
├── retriever/
│   ├── __init__.py
│   ├── config_manager.py
│   ├── default_configs.py
│   ├── retrievers.py
│   └── section.py
├── .env.example                # Arquivo de exemplo para variáveis de ambiente
├── pipeline_configs.json       # Configurações dos pipelines
├── retriever_configs.json      # Configurações dos retrievers
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação principal do projeto

Visão Geral da Arquitetura
api/: Contém toda a lógica da API web (FastAPI).

routers/: Define os endpoints, agrupados por funcionalidade (usuários, documentos, etc.). É a porta de entrada para as requisições.

schemas/: Contém os modelos Pydantic, que definem a "forma" dos dados que entram e saem da API, garantindo validação e documentação automática.

crud/: Camada de "Create, Read, Update, Delete". Abstrai a lógica de manipulação dos dados, seja de um banco de dados de usuários ou de arquivos de configuração.

dependencies.py: Gerencia a injeção de dependências, como obter o usuário logado ou uma instância de um pipeline.

main.py: Ponto de entrada que monta a aplicação FastAPI, incluindo os routers e middlewares.

database/: Responsável pela interação com os dados brutos e os vectorstores.

metadata_split/: Contém seus scripts customizados para processar cada tipo de documento.

ingestion.py: Orquestra o processo de reindexação, usando seus scripts customizados.

vectorstore_handler.py: Abstrai a criação e o carregamento dos vectorstores FAISS.

retriever/ e pipeline/: Contêm a lógica principal da sua IA, agora configurável dinamicamente através de arquivos JSON gerenciados pela API.

Arquivos de Configuração (.json): Armazenam os parâmetros dos retrievers e pipelines, permitindo alterações em tempo real via API sem a necessidade de reiniciar o servidor.

Estrutura de Diretórios Final
.
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── security.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user_crud.py
│   │   ├── retriever_crud.py
│   │   └── pipeline_crud.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── documents.py
│   │   ├── users.py
│   │   ├── retrievers.py
│   │   ├── pipelines.py
│   │   └── system.py
│   └── schemas/
│       ├── __init__.py
│       ├── chat.py
│       ├── document.py
│       ├── user.py
│       ├── retriever.py
│       ├── pipeline.py
│       └── system.py
├── database/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── vectorstore_handler.py
│   └── metadata_split/
│       ├── markdown_gerente.py
│       ├── markdown_indicadores.py
│       └── ... (todos os seus outros processadores)
├── pipeline/
│   ├── __init__.py
│   ├── config_manager.py
│   ├── handler.py
│   └── utils.py
├── retriever/
│   ├── __init__.py
│   ├── config_manager.py
│   ├── default_configs.py
│   ├── retrievers.py
│   └── section.py
├── .env.example                # Arquivo de exemplo para variáveis de ambiente
├── pipeline_configs.json       # Configurações dos pipelines
├── retriever_configs.json      # Configurações dos retrievers
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação principal do projeto

Conteúdo dos Arquivos Principais
A seguir, o conteúdo dos arquivos mais importantes, com documentação detalhada.

README.md - Documentação Principal
# API do Chatbot com RAG - Documentação do Projeto

Esta é uma API robusta construída com FastAPI para servir um sistema de Inteligência Artificial baseado em RAG (Retrieval-Augmented Generation). A API permite interações de chat, gerenciamento de usuários, configuração dinâmica dos componentes de IA e reindexação da base de conhecimento em tempo real.

## Arquitetura

O projeto é organizado em uma arquitetura de camadas para garantir manutenibilidade e escalabilidade:

- **Camada de API (`/api`)**: Responsável por expor os endpoints, lidar com requisições HTTP, validação de dados e autenticação.
- **Camada de Lógica de Negócio (`/api/crud`)**: Contém a lógica para manipular os recursos da aplicação (usuários, configurações).
- **Camada de IA (`/pipeline`, `/retriever`)**: Contém a lógica principal do sistema de RAG, incluindo a criação de pipelines e a recuperação de informações.
- **Camada de Dados (`/database`)**: Gerencia o acesso aos dados, incluindo a ingestão de documentos e a interação com os vectorstores FAISS.

## Funcionalidades

- **Autenticação de Usuários**: Sistema completo com login, gerenciamento de perfil e controle de acesso baseado em funções (usuário/admin).
- **Gerenciamento de Documentos**: Endpoints para adicionar e remover documentos (`.md`) da base de conhecimento.
- **Reindexação Dinâmica**: Um endpoint (`/system/reindex`) que dispara um processo em background para recriar os vectorstores FAISS com base nos documentos atuais, tornando a IA ciente de novas informações sem reiniciar a aplicação.
- **Configuração Dinâmica**: Endpoints para visualizar e **alterar em tempo real** os hiperparâmetros dos **Retrievers** (ex: `k`, `fetch_k`) e dos **Pipelines** (ex: `model`, `temperature`), com as alterações sendo salvas em arquivos `.json`.
- **Chat**: Endpoint principal para interagir com a IA, utilizando memória de conversação por sessão.

## Setup e Instalação

### 1. Pré-requisitos

- Python 3.10+
- Um ambiente virtual (recomendado)

### 2. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto a partir do `.env.example` e preencha os valores:

```bash
# .env
GEMINI_API_KEY="sua_chave_de_api_do_google_aqui"
SECRET_KEY="uma_chave_secreta_forte_gerada_com_openssl_rand_hex_32"

3. Instalação das Dependências
pip install -r requirements.txt

4. Executando a API
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload

A API estará disponível em http://localhost:8001. A documentação interativa (Swagger UI) pode ser acessada em http://localhost:8001/docs.

Fluxo de Trabalho Típico
Fazer Login: Use o endpoint POST /users/login com as credenciais de administrador (admin@example.com / a-very-secure-password) para obter um token de acesso.

Autorizar: Na interface do Swagger (/docs), clique no botão "Authorize" e cole o token (ex: Bearer seu_token_aqui).

Adicionar Documento: Use POST /documents para adicionar um novo arquivo .md.

Reindexar: Chame POST /system/reindex para que a IA processe o novo documento. Monitore os logs do servidor para ver o progresso.

Ajustar Parâmetros: Use os endpoints PUT em /retrievers/configurations/{section} e /pipelines/configurations/{pipeline_name} para ajustar o comportamento da IA.

Conversar: Use POST /chat/multi para interagir com a IA, que agora possui o novo conhecimento e as novas configurações.