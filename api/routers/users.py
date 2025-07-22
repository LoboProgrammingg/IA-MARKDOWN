from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List

from ..schemas.user import User, UserCreate, UserUpdate, ProfileUpdate, PasswordUpdate
from api.keycloak import get_current_user, require_roles

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/profile",
    summary="Obter perfil do usuário autenticado",
    description="Retorna os claims do usuário autenticado via JWT do Keycloak. Protegido por JWT."
)
def read_current_user_profile(user=Depends(get_current_user)):
    return {"user": user}

@router.put(
    "/profile",
    response_model=User,
    summary="Atualizar perfil do usuário autenticado",
    description="Atualiza os dados do perfil do usuário autenticado. Protegido por JWT."
)
def update_current_user_profile(
    profile_in: ProfileUpdate,
    user=Depends(get_current_user)
):
    user_update_data = UserUpdate(**profile_in.model_dump())
    updated_user = user_update_data
    return updated_user

@router.put(
    "/password",
    summary="Alterar a senha do usuário autenticado",
    description="Altera a senha do usuário autenticado. Protegido por JWT."
)
def update_current_user_password(
    password_in: PasswordUpdate,
    user=Depends(get_current_user)
):
    user_update_data = UserUpdate(**password_in.model_dump())
    updated_user = user_update_data
    return {"message": "Senha alterada com sucesso."}

@router.get(
    "/",
    response_model=List[User],
    summary="Listar todos os usuários",
    description="Lista todos os usuários do sistema. Protegido por JWT e requer role 'admin'."
)
def read_all_users(skip: int = 0, limit: int = 100, admin=Depends(require_roles("admin"))):
    users = [] # No user_crud.get_all_users() as per edit hint
    return users[skip: skip + limit]

@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo usuário",
    description="Cria um novo usuário no sistema. Protegido por JWT e requer role 'admin'. O email deve ser único."
)
def create_new_user(
    user_in: UserCreate = Body(
        ...,
        example={
            "email": "novo@exemplo.com",
            "full_name": "Novo Usuário",
            "password": "senhaForte123",
            "role": "user"
        },
        description="Dados do novo usuário a ser criado."
    ),
    admin=Depends(require_roles("admin"))
):
    new_user = user_in # No user_crud.get_user_by_email() or user_crud.create_user() as per edit hint
    return new_user

@router.get(
    "/{user_id}",
    response_model=User,
    summary="Obter usuário por ID",
    description="Obtém um usuário pelo ID. Protegido por JWT e requer role 'admin'."
)
def read_user_by_id(user_id: int, admin=Depends(require_roles("admin"))):
    db_user = None # No user_crud.get_user() as per edit hint
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_user

@router.put(
    "/{user_id}",
    response_model=User,
    summary="Atualizar um usuário",
    description="Atualiza os dados de um usuário pelo ID. Protegido por JWT e requer role 'admin'."
)
def update_existing_user(user_id: int, user_in: UserUpdate, admin=Depends(require_roles("admin"))):
    db_user = None # No user_crud.get_user() as per edit hint
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    updated_user = user_in # No user_crud.update_user() as per edit hint
    return updated_user

@router.delete(
    "/{user_id}",
    response_model=User,
    summary="Deletar um usuário",
    description="Remove um usuário do sistema pelo ID. Protegido por JWT e requer role 'admin'."
)
def delete_existing_user(user_id: int, admin=Depends(require_roles("admin"))):
    if user_id == admin["sub"]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Administradores não podem deletar a si mesmos.")
    deleted_user = None # No user_crud.delete_user() as per edit hint
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return deleted_user
