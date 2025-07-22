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
│   │   ├── token_crud.py
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

Como Funciona o Novo Fluxo de Segurança?
O processo agora envolve dois tipos de tokens, cada um com uma responsabilidade diferente:

1. Login (POST /auth/login)

O usuário envia o email e a senha, como antes.

Se as credenciais estiverem corretas, a API agora retorna dois tokens:

Um access_token de curta duração (configurado para 30 minutos).

Um refresh_token de longa duração (configurado para 7 dias).

O frontend (cliente) deve armazenar ambos os tokens de forma segura.

2. Acessando Endpoints Protegidos (ex: /chat, /documents)

Para cada requisição a um endpoint protegido, o frontend envia apenas o access_token no cabeçalho Authorization.

A API valida este token. Se for válido e não tiver expirado, a requisição é processada.

3. Quando o access_token Expira (Após 30 minutos)

A API irá retornar um erro 401 Unauthorized.

O frontend, ao receber este erro, não redireciona o usuário para a tela de login.

Em vez disso, ele faz uma chamada silenciosa para o novo endpoint POST /auth/refresh, enviando o refresh_token que estava guardado.

A API valida o refresh_token. Se for válido, ela gera um novo par de access_token e refresh_token.

O frontend substitui os tokens antigos pelos novos e refaz a requisição original que havia falhado. Para o usuário, tudo isso é transparente, e ele continua navegando sem interrupções.

4. Logout (POST /auth/logout)

Quando o usuário clica em "Logout", o frontend envia o access_token atual para este endpoint.

A API extrai o identificador único do token (jti) e o adiciona a uma "lista de bloqueio" (denylist) em memória.

O frontend então apaga os dois tokens do seu armazenamento.

Resultado: Mesmo que o access_token ainda não tenha expirado, ele não poderá mais ser usado, pois a API sempre verificará a denylist. Isso garante um logout efetivo e imediato.

Por que Este é o Melhor Padrão de Segurança?
Sim, esta implementação segue as melhores práticas por vários motivos cruciais:

Minimização da Exposição (Princípio da Segurança): O access_token, que é enviado em todas as requisições e está mais exposto a interceptações, tem uma vida útil muito curta (30 minutos). Isso limita drasticamente o dano que um token roubado pode causar.

Melhor Experiência do Usuário: O refresh_token de longa duração permite que o usuário permaneça logado por dias ou semanas sem precisar digitar a senha novamente, pois o processo de atualização do access_token é automático e invisível.

Logout Seguro e Efetivo: JWTs por natureza são "stateless" (sem estado), o que significa que um token é válido até expirar. A implementação da denylist resolve este problema, permitindo que você invalide um token ativamente no servidor, o que é essencial para um logout seguro.

Segredos Separados: Usamos chaves secretas diferentes para assinar os access_token e refresh_token. Isso é uma camada extra de segurança. Se a chave do access token fosse comprometida, a chave do refresh token (que é mais poderosa) permaneceria segura.

Em resumo, você agora tem um sistema de autenticação que é ao mesmo tempo muito seguro e amigável para o usuário final, exatamente como as grandes aplicações do mercado funcionam.

## Checklist de Melhoria e Padrões FastAPI

- [x] Centralização de configurações sensíveis e variáveis de ambiente em `settings.py` usando Pydantic/BaseSettings
- [x] Padronização de todas as respostas da API (sucesso e erro) usando schemas Pydantic e utilitário de resposta padrão
- [x] Implementação de tratamento global de erros (exception handlers) para HTTPException, ValidationError e erros inesperados
- [x] Adição de exemplos e descrições detalhadas nos principais schemas Pydantic e endpoints
- [x] Criação do endpoint `/health` para monitoramento e verificação de status da API
- [x] Configuração do CORS para aceitar apenas domínios do frontend em produção (ajustável via settings)
- [ ] Adição de rate limiting nos endpoints sensíveis
- [ ] Substituição de prints por logging estruturado
- [ ] Criação de testes automatizados para os principais endpoints
- [ ] Revisão de proteção de endpoints (autenticação e autorização por role)
- [ ] Adição de paginação e filtros nos endpoints de listagem
- [ ] Padronização e documentação de respostas de erro (schema comum para erros)

## Changelog das Implementações

### Centralização de Configurações
- Criado `settings.py` usando Pydantic/BaseSettings para centralizar variáveis sensíveis e de ambiente.
- Permite fácil ajuste de configurações para diferentes ambientes (dev/prod).

### Padronização de Respostas
- Criado `responses.py` com schemas `ApiResponse` e `ApiError`.
- Funções utilitárias para respostas padronizadas de sucesso e erro.
- Todos os endpoints e handlers globais agora usam esse padrão.

### Tratamento Global de Erros
- Adicionados exception handlers para `HTTPException`, `RequestValidationError` e erros inesperados.
- Todas as respostas de erro seguem o padrão `ApiError`.

### Documentação e Exemplos
- Adicionados exemplos e descrições detalhadas nos principais schemas Pydantic (`User`, `Token`, etc).
- Endpoints importantes agora possuem `summary`, `description` e exemplos de payload.

### Endpoint de Healthcheck
- Criado endpoint `/health` para monitoramento automatizado.
- Retorna resposta padronizada indicando se a API está saudável.

### Configuração de CORS
- Agora o CORS é configurável via variável de ambiente `CORS_ALLOWED_ORIGINS`.
- Permite restringir origens em produção e liberar em desenvolvimento.

## Configuração de CORS (Cross-Origin Resource Sharing)

A API permite configurar as origens permitidas para requisições CORS via variável de ambiente `CORS_ALLOWED_ORIGINS`.

- Para desenvolvimento, use `*` para liberar todas as origens:
  
  ```env
  CORS_ALLOWED_ORIGINS=*
  ```
- Para produção, defina os domínios do seu frontend separados por vírgula:
  
  ```env
  CORS_ALLOWED_ORIGINS=https://meufrontend.com,https://outro.com
  ```

A configuração é lida automaticamente pelo `settings.py` e aplicada no `main.py`.

## Configuração do Redis para Rate Limiting

A API utiliza o Redis para controle de rate limiting (limite de requisições por IP/usuário).

- Para desenvolvimento local, use:
  ```env
  REDIS_URL=redis://localhost:6379/0
  ```
- Para produção na Google Cloud Platform, utilize o endpoint do Redis gerenciado (memorystore) fornecido pelo GCP:
  ```env
  REDIS_URL=redis://<ENDERECO_DO_REDIS_GCP>:6379/0
  ```

A configuração é lida automaticamente pelo `settings.py`.

## Rate Limiting (Limite de Requisições)

A API utiliza rate limiting para proteger endpoints sensíveis contra abuso e ataques de força bruta.

- O endpoint `/auth/login` está limitado a 5 tentativas por minuto por IP.
- O controle é feito via Redis e FastAPI-Limiter.
- Para ajustar o limite, altere o parâmetro `RateLimiter(times=5, seconds=60)` no endpoint desejado.

O rate limiting é inicializado automaticamente na inicialização da API, usando a configuração de Redis definida em `settings.py`.

## Logging Estruturado (Cloud/GCP Friendly)

A API utiliza o módulo `logging` do Python para registrar logs de inicialização, avisos e erros.

- Em produção (`ENVIRONMENT=production`), os logs são emitidos em formato JSON, compatível com Stackdriver Logging (Google Cloud Logging).
- Em desenvolvimento, os logs são emitidos em texto simples para facilitar leitura local.
- Todos os prints foram substituídos por `logging.info`, `logging.warning` ou `logging.exception`.

Para customizar o formato ou o nível de logging, ajuste a configuração no início do arquivo `main.py`.

## Testes Automatizados

A API possui testes automatizados usando `pytest`, `httpx` e `pytest-asyncio`.

- Os testes estão localizados na pasta `tests/`.
- Para rodar todos os testes, execute:
  ```bash
  pytest
  ```
- Os testes cobrem endpoints principais como `/` (root), `/health` e podem ser expandidos para autenticação, criação de usuário, etc.

Para adicionar novos testes, crie arquivos na pasta `tests/` seguindo o padrão `test_*.py`.

---

As próximas implementações seguirão este checklist e serão documentadas aqui conforme avançarmos.