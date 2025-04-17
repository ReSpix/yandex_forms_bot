FROM python:3.12.4-slim

WORKDIR /app

COPY ./api/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api .
COPY ./nats_wrapper ./nats_wrapper

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
