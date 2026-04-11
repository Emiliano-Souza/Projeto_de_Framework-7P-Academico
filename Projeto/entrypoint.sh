#!/bin/sh
set -e

echo "Esperando o banco subir..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Banco pronto."

echo "Rodando migrations..."
python manage.py migrate --noinput

echo "Subindo servidor..."
exec python manage.py runserver 0.0.0.0:8000
