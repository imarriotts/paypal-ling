from fastapi import APIRouter, Depends, HTTPException
from app.services.redis_service import get_paypal_jwt_token, get_paypal_payment_link, store_paypal_payment_link
from app.services.paypal_service import generate_payment_link
from app.utils.responses import standard_response
from app.core.security import validate_jwt_token
from app.models.payment import PaymentUrlResponse, StandardResponsePayment, PaymentRequest, PaymentResponse
from fastapi.security import OAuth2PasswordBearer
import uuid

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/api/payment/generate", response_model=StandardResponsePayment, tags=["Pagos"])
async def generate_payment(payment: PaymentRequest, token: str = Depends(oauth2_scheme)):
    """Genera un link de pago de PayPal y devuelve el id."""
    # internal payment id
    payment_id = str(uuid.uuid4())

    # obtiene los datos del request
    amount = payment.amount
    expiration = payment.expires_in

    # valida token
    payload = validate_jwt_token(token)

    # obtiene el id del cliente
    client_id = payload["id"]

    if not client_id:
        raise Exception("Token no válido")

    # obtiene el token de paypal
    paypal_token = get_paypal_jwt_token(client_id)

    if not paypal_token:
        raise Exception("Token de PayPal no encontrado")

    # genera link de pago paypal
    payment_link = generate_payment_link(paypal_token, amount)

    # guarda el link de pago en redis
    store_paypal_payment_link(payment_id, payment_link, expiration)

    # genera response
    response = PaymentResponse(id=payment_id)

    # retorna
    return standard_response(response.model_dump())


@router.get("/api/payment/{payment_id}", tags=["Pagos"])
async def get_payment(payment_id: str, token: str = Depends(oauth2_scheme)):
    """Obtiene el link de pago de PayPal y redirecciona al link."""
    try:
        # Valida token y obtiene payload
        payload = validate_jwt_token(token)
        client_id = payload.get("id")

        if not client_id:
            raise HTTPException(status_code=401, detail="Token no válido")

        # Obtiene el link de pago de redis
        payment_link = get_paypal_payment_link(payment_id)

        if not payment_link:
            raise HTTPException(status_code=404, detail="Link de pago no encontrado")

        # Genera response
        response = PaymentUrlResponse(url=payment_link)

        # Redirecciona al link de pago
        return standard_response(response.model_dump())


    except Exception as e:
        # Maneja otros errores no anticipados
        raise HTTPException(status_code=500, detail=str(e))