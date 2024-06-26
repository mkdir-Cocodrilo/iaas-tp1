# Utiliser l'image officielle de Python
FROM python:3.9-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean

ENV TZ=Europe/Paris

# Copier les fichiers de l'application
COPY . /app
WORKDIR /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port
EXPOSE 8080

# Démarrer cron et l'application FastAPI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8080"]
