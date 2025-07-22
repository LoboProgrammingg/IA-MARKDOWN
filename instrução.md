Backend (FastAPI)

### Progresso/Implementação

1. **Configurar integração com Keycloak para autenticação JWT**
   - [x] Middleware de autenticação JWT implementado usando dependência `get_current_user` do Keycloak
   - [x] Validação de tokens com chave pública do Keycloak (JWKS)
   - [x] Variáveis de ambiente para configuração do Keycloak (`KEYCLOAK_URL`, `KEYCLOAK_REALM`, `KEYCLOAK_CLIENT_ID`, `KEYCLOAK_CLIENT_SECRET`, `KEYCLOAK_AUDIENCE`)
   - [x] Decorators de autorização por roles/permissions (`require_roles`)
   - [x] Endpoint para refresh token faz proxy para o Keycloak
   - [x] Login/logout local removidos. Toda autenticação agora é feita exclusivamente via Keycloak.
   - [x] Documentação dos endpoints e README atualizados para uso com Keycloak

**Como obter e usar o token JWT do Keycloak:**

1. Faça uma requisição POST para:
   `http://<KEYCLOAK_HOST>/realms/<REALM>/protocol/openid-connect/token`
   com os campos:
   - `grant_type=password`
   - `client_id=<CLIENT_ID>`
   - `client_secret=<CLIENT_SECRET>` (se necessário)
   - `username=<USUÁRIO>`
   - `password=<SENHA>`
2. Use o `access_token` retornado no header:
   `Authorization: Bearer <access_token>`

Todos os endpoints protegidos exigem JWT do Keycloak. Endpoints sensíveis exigem roles específicos (ex: `admin`).

2. **Remover hard codes e substituir por variáveis de ambiente**
   - [x] Uso de `settings.py` com Pydantic/BaseSettings para centralizar configurações.
   - [ ] Garantir que todas as strings sensíveis e conexões estejam em variáveis de ambiente.
   - [ ] Criar/atualizar `.env.example`.

3. **Alterar banco de dados - postgres**
   - [ ] Instalar/configurar pgvector.
   - [ ] Migrar dados do vectorstore para PostgreSQL.
   - [ ] Atualizar queries para usar PostgreSQL.
   - [ ] Configurar conexão no settings.

4. **Remover conteúdo depreciado**
   - [ ] Remover código/imports/arquivos obsoletos.
   - [ ] Limpar requirements.txt.

5. **Atualizar dependências**
   - [x] Adicionado `uvicorn[standard]` ao requirements.txt.

6. **Atualizar documentação**
   - [x] Documentação de variáveis de ambiente e setup local no README.
   - [ ] Documentar novos endpoints de IA e exemplos de uso.
   - [ ] Garantir documentação OpenAPI detalhada.

---

**Como utilizar autenticação JWT com Keycloak:**
- Adicione o token JWT do Keycloak no header `Authorization: Bearer <token>` em cada requisição protegida.
- Use a dependência `get_current_user` do `keycloak.py` nos endpoints que exigem autenticação.
- Exemplo de uso em um endpoint:

```python
from api.keycloak import get_current_user
from fastapi import Depends

@router.get("/profile")
def get_profile(user=Depends(get_current_user)):
    return {"user": user}
```

---

   - [x] Criar endpoints para refresh token.
     - Endpoint `POST /auth/refresh` criado. Recebe um refresh_token e retorna novo access_token/refresh_token do Keycloak.
     - O backend faz proxy para o endpoint oficial do Keycloak, usando as variáveis de ambiente de configuração.
     - Exemplo de uso:
       ```http
       POST /auth/refresh
       Content-Type: application/json
       {
         "refresh_token": "<refresh_token>"
       }
       ```
   - [x] Criar endpoint POST /contexts para inserir contextos.
     - Endpoint `POST /contexts` criado em `routers/contexts.py`.
     - Protegido por autenticação JWT do Keycloak.
     - Payload validado pelo schema `ContextCreate`.
     - Exemplo de uso:
       ```http
       POST /contexts
       Content-Type: application/json
       Authorization: Bearer <token>
       {
         "nome": "Meu contexto",
         "descricao": "Descrição do contexto",
         "dados": {"chave": "valor"}
       }
       ```
   - [x] Criar endpoint POST /templates para gerenciar templates.
     - Endpoint `POST /templates` criado em `routers/templates.py`.
     - Protegido por autenticação JWT do Keycloak e exige role `admin`.
     - Payload validado pelo schema `Template`.
     - Exemplo de uso:
       ```http
       POST /templates
       Content-Type: application/json
       Authorization: Bearer <token_admin>
       {
         "name": "resumo_tecnico",
         "content": "Resuma o seguinte texto: {texto}",
         "description": "Template para resumos técnicos."
       }
       ```
   - [x] Criar endpoint POST /prompts para gerenciar prompts.
     - Endpoint `POST /prompts` criado em `routers/prompts.py`.
     - Protegido por autenticação JWT do Keycloak e exige role `admin`.
     - Payload validado pelo schema `Prompt`.
     - Exemplo de uso:
       ```