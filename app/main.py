import traceback
from fastapi import FastAPI, HTTPException, Request
from .api import auth
from .api import payment
from .utils import responses
from uvicorn import run

app = FastAPI(docs_url="/docs")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return responses.error_response(code=exc.status_code, message=str(exc.detail))

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return responses.error_response(code=400, message=str(exc))

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    error_message = str(exc)
    stack_trace = traceback.format_exc()
    return responses.error_response(code=500, message=error_message, error_data=stack_trace)

# se incluyen los routers
app.include_router(auth.router)
app.include_router(payment.router)

@app.get("/", tags=["root"], summary="Inicio", description="Servicio de generación de pagos con PayPal")
async def root():
    return responses.standard_response({"message": "Servicio de generación de pagos con PayPal"})

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)