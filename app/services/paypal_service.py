import json
import requests
from app.core.config import settings
from typing import Tuple

PAYPAL_URL = settings.paypal_url

def authenticate_paypal(client_id: str, client_secret: str) -> Tuple[str, int]:
    """Autentica con PayPal y devuelve el token de acceso."""

    PAYPAL_LOGIN_API = f"{PAYPAL_URL}/v1/oauth2/token"
    PAYPAL_HEADERS = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    PAYPAL_DATA = {'grant_type': 'client_credentials'}
    PAYPAL_AUTH = (client_id, client_secret)

    # llamar a la API de PayPal
    auth_response = requests.post(PAYPAL_LOGIN_API, headers=PAYPAL_HEADERS, data=PAYPAL_DATA, auth=PAYPAL_AUTH)

    # verificar que la respuesta sea 200
    if auth_response.status_code == 200:

        # castear la respuesta a JSON
        auth_response_json = auth_response.json()

        # obtiene el token de acceso y exp
        token = auth_response_json['access_token']
        exp = auth_response_json['expires_in']

        if not token:
            raise Exception("No se pudo obtener el token de PayPal")

        # return access_token
        return token, exp
    else:
        raise Exception(f"Fallo al autenticar con PayPal")


def generate_payment_link(access_token: str, value: float = 10.00) -> str:
    """Genera un link de pago de PayPal y devuelve el link."""
    PAYPAL_API = f"{PAYPAL_URL}/v1/payments/payment"

    PAYPAL_HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    
    PAYPAL_DATA = {
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'transactions': [{
            'amount': {
                'total': str(value),
                'currency': 'USD',
            },
            'description': 'Pago',
        }],
        'redirect_urls': {
            'return_url': 'http://example.com/return',
            'cancel_url': 'http://example.com/cancel',
        },
    }

    # llamar a la API de PayPal
    payment_response = requests.post(PAYPAL_API, headers=PAYPAL_HEADERS, data=json.dumps(PAYPAL_DATA))

    # verificar que la respuesta sea 200
    if payment_response.status_code != 201:
        raise Exception(f"Fallo al generar el link de pago con PayPal")
    
    # castear la respuesta a JSON
    payment_response_json = payment_response.json()

    approval_url = None

    # obtener el link de aprobación
    for link in payment_response_json['links']:
        if link['rel'] == 'approval_url':
            approval_url = link['href']
            break

    return approval_url
