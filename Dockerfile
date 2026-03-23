FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \n    gcc \n    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data

EXPOSE 8000 8001

ENV PYTHONUNBUFFERED=1
ENV DB_FILE=/app/data/my_database.duckdb

CMD ["python", "main.py"]