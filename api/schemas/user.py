from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário, usado para login.", example="usuario@exemplo.com")
    full_name: Optional[str] = Field(None, description="Nome completo do usuário.", example="João da Silva")
    is_active: bool = Field(True, description="Indica se o usuário está ativo.", example=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Senha do usuário.", example="senhaSegura123")
    role: str = Field("user", description="Função do usuário ('user' ou 'admin').", example="user")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Novo email do usuário.", example="novo@exemplo.com")
    full_name: Optional[str] = Field(None, description="Novo nome completo.", example="Maria Oliveira")
    is_active: Optional[bool] = Field(None, description="Ativar/desativar usuário.", example=False)
    role: Optional[str] = Field(None, description="Nova função ('user' ou 'admin').", example="admin")

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, description="Novo nome completo.", example="Carlos Souza")
    email: Optional[EmailStr] = Field(None, description="Novo email.", example="carlos@exemplo.com")

class PasswordUpdate(BaseModel):
    current_password: str = Field(..., description="A senha atual do usuário.", example="senhaAntiga123")
    new_password: str = Field(..., min_length=8, description="A nova senha do usuário.", example="novaSenha456")

class User(UserBase):
    id: int = Field(..., description="ID único do usuário.", example=1)
    role: str = Field(..., description="Função do usuário ('user' ou 'admin').", example="admin")
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str = Field(..., description="Senha do usuário criptografada.")