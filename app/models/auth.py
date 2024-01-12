from pydantic import BaseModel

class Token(BaseModel):
    """Modelo de response para el endpoint de generación de jwt."""
    token: str

class StandardResponseToken(BaseModel):
    code: int
    success: bool
    data: Token