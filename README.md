# Aplicación FastAPI: Servicio de Generación de Links de Pago con PayPal

## Descripción General del Proyecto

Esta aplicación de FastAPI, llamada `paypal-link`, está diseñada para facilitar la generación de links de pago con PayPal. Incluye funcionalidades de autenticación, generación de links de pago y redirección a PayPal. Este proyecto soporta Docker, lo que facilita su despliegue y asegura la consistencia del entorno.

## Estructura del Proyecto

```
app/                             # Directorio principal de la aplicación FastAPI
    api/                         # Endpoints de la API
        auth.py                  # Endpoint para la autenticación
        payment.py               # Endpoints para la gestión de pagos
    core/                        # Configuración y seguridad
        config.py                # Configuración de la aplicación
        security.py              # Lógica de seguridad y JWT
    models/                      # Modelos de datos
        user.py                  # Modelo de usuario
        payment.py               # Modelo de pago
    services/                    # Lógica de servicios
        paypal_service.py        # Servicio de interacción con PayPal
        redis_service.py         # Servicio de manejo de Redis
    utils/                       # Utilidades y herramientas
        responses.py             # Envoltorios para respuestas de API
    main.py                      # Punto de entrada de la aplicación FastAPI
Dockerfile                       # Instrucciones para construir la imagen de Docker
docker-compose.yml               # Orquestación de Docker para la app y Redis
.env                             # Variables de entorno
.gitignore                       # Especifica patrones a excluir en Git
README.md                        # Este archivo
requirements.txt                 # Dependencias del proyecto
```

## Requerimientos

Antes de comenzar con el desarrollo o la ejecución de este proyecto, asegúrate de tener instalados los siguientes requisitos previos:

- **Python**: Es necesario para ejecutar el servidor FastAPI.
- **Redis**: Es necesario para almacenar los links de pago generados, puedes correrlo en un contenedor Docker con `docker run --name redis -p 6379:6379 -d redis` o usar algún servicio de Redis en la nube.
- **Docker (Opcional)**: Para contenerizar la aplicación y Redis.

## Scripts Disponibles

- **Servidor Local**: Ejecuta `uvicorn app.main:app --reload` para iniciar el servidor de desarrollo con recarga en caliente, recuerda tener una instancia de Redis ejecutándose localmente si deseas probar la aplicación. El servidor se ejecutará en `http://localhost:8000`
- **Docker**: Usa `docker-compose up --build` seguido de `docker-compose up` para construir y ejecutar la aplicación y Redis en contenedores Docker.

## Debugging
Se utilizo el debugger de VSCode. Para esto se creo el archivo `launch.json` en la carpeta `.vscode` que contiene la configuración para lanzar la aplicación en modo debug.

## Dockerización de la Aplicación

El `Dockerfile` y `docker-compose.yml` proporcionan las instrucciones para contenerizar la aplicación junto con Redis, facilitando su despliegue y operación en cualquier entorno que soporte Docker.

## APIs y Rutas

La aplicación `paypal-link` ofrece varias rutas para manejar la autenticación y los pagos:

### Autenticación - `/api/auth`

- `GET /api/auth/login`: Endpoint para autenticación. Genera un token JWT tras autenticar con PayPal.

Este servicio recibe como basic auth las credenciales de PayPal, y devuelve un token JWT que debe ser incluido en el header `authorization` de las peticiones a los endpoints protegidos.

### Generación y Manejo de Pagos - `/api/payment`

- `POST /api/payment/generate`: Endpoint para generar un link de pago con PayPal, requiere autenticación por JWT y recibe como parámetro el monto del pago y la expiración del link.
- `GET /api/payment/{payment_id}`: Endpoint para obtener un link de pago, requiere autenticación por JWT y recibe como parámetro el ID del pago.

### Documentación Swagger UI

- La documentación Swagger UI está disponible en `/docs`. Esta interfaz ofrece una documentación interactiva y visual de todas las rutas de la API, permitiendo a los usuarios probar los endpoints directamente desde el navegador.

## Detalles Adicionales de las Rutas

- **Manejo de Errores**: Cada ruta incluye un manejo robusto de errores para proporcionar respuestas informativas en caso de problemas.
- **Validaciones**: Se aplican validaciones para asegurar que las entradas de los usuarios cumplan con los requisitos esperados. Esto incluye la validación de tokens JWT, montos de pago, y otros parámetros de entrada.
- **Autenticación y Seguridad**: Las rutas sensibles están protegidas mediante autenticación JWT, asegurando que solo los usuarios autenticados puedan acceder a ciertas funcionalidades.
- **Integración con PayPal**: La aplicación se integra con la API de PayPal para generar links de pago y manejar transacciones.
