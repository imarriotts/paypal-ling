from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.utils import responses
from app.services.redis_service import store_paypal_jwt_token
from app.services.paypal_service import authenticate_paypal
from app.core.security import create_jwt_token
from app.models.auth import Token, StandardResponseToken

router = APIRouter()
security = HTTPBasic()

@router.get("/api/auth/login",
            response_model=StandardResponseToken,
            summary="Genera Token JWT",
            description="Autentica al usuario con PayPal y devuelve un token JWT.",
            response_description="Token JWT",
            tags=["Autenticación"]
            )
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    """Autentica al usuario con PayPal y devuelve un token JWT."""
    client_id = credentials.username
    client_secret = credentials.password

    # Autenticar con PayPal, obtener el token y expiración
    paypal_token, paypal_token_exp = authenticate_paypal(client_id, client_secret)

    # Guardar el token de PayPal en redis
    store_paypal_jwt_token(paypal_token, client_id, paypal_token_exp)

    # generar un token JWT con el id del cliente
    jwt_token = create_jwt_token(client_id)

    # generar el response 
    response = Token(token=jwt_token)

    # devolver el token JWT
    return responses.standard_response(response.model_dump())
