FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependências de sistema (build e Java para Spark)
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY public ./public
EXPOSE 8000

# Executar somente a aplicação FastAPI
CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
