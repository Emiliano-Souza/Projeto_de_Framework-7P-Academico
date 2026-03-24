#!/bin/sh
set -e

echo "Esperando o banco subir..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Banco pronto."

if [ ! -f manage.py ]; then
  echo "Criando projeto Django..."
  django-admin startproject config .

  python <<'PY'
from pathlib import Path
import re

p = Path("config/settings.py")
s = p.read_text()

s = re.sub(r"ALLOWED_HOSTS = \[\]", "ALLOWED_HOSTS = ['*']", s)

s += """

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'epi_db'),
        'USER': os.environ.get('POSTGRES_USER', 'epi_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '123456'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
"""
p.write_text(s)
PY
fi

python manage.py migrate --noinput

exec python manage.py runserver 0.0.0.0:8000