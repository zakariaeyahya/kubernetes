import streamlit as st
import requests
import json
import pandas as pd
import os
import logging
from urllib.parse import urljoin

# Configuration de la page
st.set_page_config(
    page_title="Explorateur de Métiers IT",
    page_icon="💼",
    layout="wide"
)

# Configuration des logs avec plus de détails
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# URL du backend (utilisation de la variable d'environnement ou valeur par défaut)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')
logger.info(f"Backend URL configured as: {BACKEND_URL}")

def get_similar_jobs(job_title: str, top_n: int = 5):
    """Appelle l'API pour obtenir les métiers similaires"""
    try:
        # Construction de l'URL
        endpoint = urljoin(BACKEND_URL, "find_similar_jobs")
        logger.info(f"Making request to endpoint: {endpoint}")
        
        # Préparation des données
        payload = {
            "job_title": job_title,
            "top_n": top_n
        }
        logger.info(f"Request payload: {payload}")

        # En-têtes de la requête
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Envoi de la requête avec timeout et vérification SSL désactivée pour dev
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=30,
            verify=False  # Pour le développement uniquement
        )
        
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")

        # Vérification de la réponse
        if response.status_code == 200:
            try:
                data = response.json()
                logger.info("Successfully parsed response JSON")
                return data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                st.error("Erreur lors du traitement de la réponse du serveur")
                return None
        else:
            logger.error(f"Server returned error {response.status_code}: {response.text}")
            st.error(f"Le serveur a retourné une erreur {response.status_code}")
            return None

    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        st.error(f"""
        Erreur de connexion au backend:
        - URL tentée: {endpoint}
        - Erreur: Impossible de se connecter au serveur
        - Vérifiez que le service backend est accessible
        """)
        return None
    except requests.exceptions.Timeout as e:
        logger.error(f"Request timeout: {e}")
        st.error("Le serveur met trop de temps à répondre")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        st.error(f"Une erreur inattendue s'est produite: {str(e)}")
        return None

# Interface utilisateur
st.title("🔍 Explorateur de Métiers IT")
st.markdown("""
Cette application vous aide à découvrir les métiers de l'IT similaires à vos intérêts.
""")

# Zone de saisie utilisateur
job_input = st.text_input(
    "Entrez un métier IT",
    placeholder="Ex: Data Scientist, DevOps Engineer..."
)

# Nombre de résultats souhaités
top_n = st.slider(
    "Nombre de résultats à afficher",
    min_value=1,
    max_value=10,
    value=5
)

# Bouton de recherche
if st.button("Rechercher", type="primary"):
    if job_input:
        with st.spinner("Recherche en cours..."):
            results = get_similar_jobs(job_input, top_n)
            
            if results:
                st.success("Résultats trouvés!")
                
                # Affichage des résultats
                for job in results.get('similar_jobs', []):
                    with st.expander(f"🎯 {job['job_title']} (Score: {job['similarity_score']:.2%})"):
                        if 'skills' in job:
                            st.write("**Compétences requises:**")
                            st.write(", ".join(job['skills']))
    else:
        st.warning("Veuillez entrer un métier à rechercher")

# Footer avec informations de débogage
with st.expander("ℹ️ Informations de débogage"):
    st.write(f"Backend URL: {BACKEND_URL}")
    st.write("Version de l'application: 1.0.0")