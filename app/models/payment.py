from pydantic import BaseModel

class PaymentResponse(BaseModel):
    """Moodelo de response para el endpoint de generación de pagos."""
    id: str

class PaymentRequest(BaseModel):
    """Modelo de request para el endpoint de generación de pagos."""
    amount: float
    expires_in: int

class StandardResponsePayment(BaseModel):
    code: int
    success: bool
    data: PaymentResponse

class PaymentUrlResponse(BaseModel):
    url: str

class StandardResponsePaymentUrl(BaseModel):
    code: int
    success: bool
    data: PaymentUrlResponse