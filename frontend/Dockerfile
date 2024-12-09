# Utiliser une image Python officielle comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application
COPY frontend.py .

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Variable d'environnement pour l'URL de l'API backend
ENV BACKEND_URL=http://backend-service:8000

# Commande pour démarrer l'application
CMD ["streamlit", "run", "frontend.py", "--server.address", "0.0.0.0"]