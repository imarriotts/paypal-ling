# Imagen oficial de Python como imagen base
FROM python:3.9

# Establece un directorio de trabajo
WORKDIR /app

# Copiar los archivos 'requirements.txt' y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Agrega el directorio /app al PYTHONPATH
ENV PYTHONPATH=/app

# Indica el puerto que estará escuchando la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]