# Dockerfile pour déploiement production
FROM python:3.9-slim

# Métadonnées
LABEL maintainer="Prompt Maître Team"
LABEL description="API de génération automatique de prompts No Code"

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY prompt_generator.py .
COPY api_server.py .
COPY schema.json .

# Exposer le port
EXPOSE 8000

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Commande de démarrage
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
