#FROM python:3.11-slim
#
#ENV PYTHONUNBUFFERED=1
#
## Устанавливаем netcat (nc)
#RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean
#
## Устанавливаем рабочую директорию
#WORKDIR /app
#
## Копируем requirements и устанавливаем зависимости
#COPY requirements.txt .
#
#RUN pip install --no-cache-dir --upgrade pip && \
#    pip install --no-cache-dir -r requirements.txt && \
#    pip install --no-cache-dir uvicorn fastapi
#
## Копируем всё приложение
#COPY . .
#
## Убедимся, что скрипт исполняемый
##RUN chmod +x /app/docker-entrypoint.sh
#
#EXPOSE 8009
#
##ENTRYPOINT ["/app/docker-entrypoint.sh"]
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8009"]


FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    git \
    && apt-get clean

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir wheel \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8009

# Выполнение Alembic миграций ПЕРЕД запуском сервера (одной строкой)
CMD bash -c "\
    echo 'Waiting for DB at $DB_HOST:$DB_PORT...' && \
    until nc -z \$DB_HOST \$DB_PORT; do echo 'Waiting...'; sleep 1; done && \
    echo 'Waiting for RabbitMQ at $RABBITMQ_HOST:$RABBITMQ_PORT...' && \
    until nc -z \$RABBITMQ_HOST \$RABBITMQ_PORT; do echo 'Waiting...'; sleep 1; done && \
    alembic upgrade head && \
    echo 'Starting Uvicorn...' && \
    uvicorn main:app --host 0.0.0.0 --port 8009 --reload"






