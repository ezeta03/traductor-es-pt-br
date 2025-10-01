FROM python:3.10-slim

WORKDIR /app

# instalar dependencias básicas
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

# copiar requirements e instalar
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copiar el código
COPY . .

ENV PYTHONUNBUFFERED=1

# uvicorn por defecto
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
