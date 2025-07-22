from typing import Any, Optional
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

class ApiResponse(BaseModel):
    success: bool = Field(True, description="Indica se a requisição foi bem-sucedida.", example=True)
    message: Optional[str] = Field(None, description="Mensagem de sucesso ou informação adicional.", example="Operação realizada com sucesso.")
    data: Optional[Any] = Field(None, description="Dados retornados pela API.", example={"id": 1, "nome": "Exemplo"})

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Operação realizada com sucesso.",
                "data": {"id": 1, "nome": "Exemplo"}
            }
        }

class ApiError(BaseModel):
    success: bool = Field(False, description="Indica que houve erro na requisição.", example=False)
    message: str = Field(..., description="Mensagem de erro.", example="Recurso não encontrado.")
    error_code: Optional[str] = Field(None, description="Código de erro específico, se aplicável.", example="404")
    details: Optional[Any] = Field(None, description="Detalhes adicionais do erro.", example={"field": "email", "error": "inválido"})

    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "message": "Recurso não encontrado.",
                "error_code": "404",
                "details": {"field": "email", "error": "inválido"}
            }
        }

def success_response(data: Any = None, message: Optional[str] = None) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=ApiResponse(success=True, message=message, data=data).dict(exclude_none=True)
    )

def error_response(message: str, status_code: int = 400, error_code: Optional[str] = None, details: Any = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ApiError(success=False, message=message, error_code=error_code, details=details).dict(exclude_none=True)
    ) 