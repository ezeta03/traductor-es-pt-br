FROM python:3.10-slim

WORKDIR /app

# Copiamos los requirements
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos toda la carpeta app al contenedor
COPY app/ .

# Exponemos el puerto de uvicorn
EXPOSE 8000

# Arrancamos la API
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
