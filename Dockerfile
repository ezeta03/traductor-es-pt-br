FROM python:3.10-slim

WORKDIR /app

# Copiamos requirements primero para aprovechar cache
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos toda la carpeta app (se instalará como paquete local)
COPY app /app/app

# Opcional: agregar /app al PYTHONPATH para que encuentre "app"
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
