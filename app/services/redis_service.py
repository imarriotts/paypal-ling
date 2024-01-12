
import redis
from app.core.config import settings

redis_client = None

def init_redis() -> None:
    """Inicializa Cliente de Redis o retorna el cliente existente."""
    global redis_client
    if not redis_client:
        redis_client = redis.Redis.from_url(settings.redis_url)
    return redis_client

def store_paypal_jwt_token(token: str, client_id: str, exp: int = 1800) -> None:
    """Guarda el token de PayPal en Redis."""
    # obtiene un cliente de redis
    redis_client = init_redis()
    # guardar el token en redis
    redis_client.set(f"paypal_token:{client_id}", token, ex=exp)
    return None

def get_paypal_jwt_token(client_id: str) -> str:
    """Obtiene el token de PayPal de Redis."""
    # obtiene un cliente de redis
    redis_client = init_redis()
    # obtener el token de redis
    token = redis_client.get(f"paypal_token:{client_id}")
    # devolver el token
    return token.decode("utf-8") if token else None

def store_paypal_payment_link(payment_id: str, link: str, exp: int = 600000) -> None:
    """Guarda el link de pago de PayPal en Redis."""
    # obtiene un cliente de redis
    redis_client = init_redis()
    # guardar el link en redis
    redis_client.set(f"paypal_payment_link:{payment_id}", link, ex=exp)
    return None

def get_paypal_payment_link(payment_id: str) -> str:
    """Obtiene el link de pago de PayPal de Redis."""
    # obtiene un cliente de redis
    redis_client = init_redis()
    # obtener el link de redis
    link = redis_client.get(f"paypal_payment_link:{payment_id}")
    # devolver el link
    return link.decode("utf-8") if link else None