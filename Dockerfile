FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Script pentru a aștepta PostgreSQL
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

# Creează script de wait
RUN echo '#!/bin/sh\n\
while ! nc -z $DB_HOST 5432; do\n\
  echo "Waiting for postgres..."\n\
  sleep 1\n\
done\n\
echo "PostgreSQL started"\n\
python manage.py runserver 0.0.0.0:8000' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]