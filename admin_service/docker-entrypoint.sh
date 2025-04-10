#!/bin/sh

echo "🚀 Ждём базу данных на $DB_HOST:$DB_PORT..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done

echo "✅ База данных готова! Запускаем FastAPI..."

exec "$@"



