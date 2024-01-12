from fastapi.responses import JSONResponse

def standard_response(data: dict, code: int = 200):
    """Devuelve una respuesta estándar con el código 200 y el contenido especificado."""
    return JSONResponse(content={"code": 200, "success": True, "data": data})

def error_response(code: int, message: str, error_data=None):
    """Devuelve una respuesta de error con el código, mensaje y datos de error especificados."""
    if error_data is None:
        error_data = []
    content = {"code": code, "success": False, "errorData": error_data, "message": message}
    return JSONResponse(status_code=code, content=content)
