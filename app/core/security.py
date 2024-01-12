import jwt
from app.core.config import settings
from fastapi import HTTPException, status, Depends

SECRET_KEY = settings.secret_key

def create_jwt_token(client_id: str) -> str:
    """Crea un token JWT con el id del cliente"""
    payload = {"id": client_id}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def validate_jwt_token(token: str):
    """Valida el token JWT y devuelve el id del cliente"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token JWT inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
