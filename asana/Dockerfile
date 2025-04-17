FROM python:3.12.4-slim

RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./asana/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./asana .
COPY ./nats_wrapper ./nats_wrapper

CMD ["python", "main.py"]
