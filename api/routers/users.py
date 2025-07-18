from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ..schemas.user import User, UserCreate, UserUpdate, ProfileUpdate, PasswordUpdate
from ..crud import user_crud
from ..dependencies import get_current_active_user, get_current_admin_user
from ..security import verify_password

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/profile", response_model=User, summary="Obter perfil do usuário atual")
def read_current_user_profile(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/profile", response_model=User, summary="Atualizar perfil do usuário atual")
def update_current_user_profile(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_active_user)
):
    if profile_in.email and user_crud.get_user_by_email(profile_in.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Este email já está em uso.")
    
    user_update_data = UserUpdate(**profile_in.model_dump())
    updated_user = user_crud.update_user(current_user.id, user_update_data)
    return updated_user

@router.put("/password", summary="Alterar a senha do usuário atual")
def update_current_user_password(
    password_in: PasswordUpdate,
    current_user: User = Depends(get_current_active_user)
):
    db_user = user_crud.get_user(current_user.id)
    if not verify_password(password_in.current_password, db_user.hashed_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Senha atual incorreta.")
    
    user_crud.update_user_password(current_user.id, password_in.new_password)
    return {"message": "Senha alterada com sucesso."}

@router.get("/", response_model=List[User], summary="Listar todos os usuários (Admin Only)")
def read_all_users(skip: int = 0, limit: int = 100, current_admin: User = Depends(get_current_admin_user)):
    users = user_crud.get_all_users()
    return users[skip: skip + limit]

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, summary="Criar um novo usuário (Admin Only)")
def create_new_user(user_in: UserCreate, current_admin: User = Depends(get_current_admin_user)):
    db_user = user_crud.get_user_by_email(email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado.")
    new_user = user_crud.create_user(user_in=user_in)
    return new_user

@router.get("/{user_id}", response_model=User, summary="Obter usuário por ID (Admin Only)")
def read_user_by_id(user_id: int, current_admin: User = Depends(get_current_admin_user)):
    db_user = user_crud.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_user

@router.put("/{user_id}", response_model=User, summary="Atualizar um usuário (Admin Only)")
def update_existing_user(user_id: int, user_in: UserUpdate, current_admin: User = Depends(get_current_admin_user)):
    db_user = user_crud.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    if user_in.email and user_crud.get_user_by_email(user_in.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Este email já está em uso.")

    updated_user = user_crud.update_user(user_id, user_in)
    return updated_user

@router.delete("/{user_id}", response_model=User, summary="Deletar um usuário (Admin Only)")
def delete_existing_user(user_id: int, current_admin: User = Depends(get_current_admin_user)):
    if user_id == current_admin.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Administradores não podem deletar a si mesmos.")
    
    deleted_user = user_crud.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return deleted_user
