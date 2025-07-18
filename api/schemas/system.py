from pydantic import BaseModel, Field

class ReindexResponse(BaseModel):
    status: str
    message: str