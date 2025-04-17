FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Устанавливаем netcat (nc)
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
   pip install --no-cache-dir -r requirements.txt && \
   pip install --no-cache-dir uvicorn fastapi

# Копируем всё приложение
COPY . .

#Убедимся, что скрипт исполняемый
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8009

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8009"]








