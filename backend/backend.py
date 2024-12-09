from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from typing import Dict, List, Optional
import uvicorn
import logging
import os
import traceback

# Configuration détaillée des logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle avec gestion d'erreur
try:
    logger.info("Démarrage du chargement du modèle...")
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    logger.info("Modèle chargé avec succès")
except Exception as e:
    logger.error(f"Erreur lors du chargement du modèle: {str(e)}")
    logger.error(traceback.format_exc())
    raise

# Chemin vers le fichier JSON
JSON_PATH = "skills_embeddings.json"

class JobRequest(BaseModel):
    job_title: str
    top_n: Optional[int] = 5

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Exception non gérée: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": f"Erreur interne: {str(exc)}"}
    )

def load_embeddings() -> Dict:
    try:
        logger.info(f"Tentative de chargement du fichier: {JSON_PATH}")
        logger.info(f"Chemin absolu: {os.path.abspath(JSON_PATH)}")
        logger.info(f"Contenu du répertoire: {os.listdir('.')}")
        
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"Fichier JSON chargé avec succès. Taille: {len(data)} entrées")
            # Afficher la structure d'une entrée pour débogage
            first_key = next(iter(data))
            logger.info(f"Structure de la première entrée ({first_key}): {data[first_key].keys()}")
            return data
            
    except Exception as e:
        logger.error(f"Erreur lors du chargement du fichier: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du chargement des données: {str(e)}"
        )

@app.get("/")
async def root():
    return {"message": "API de similarité des métiers IT", "status": "running"}

@app.post("/find_similar_jobs")
async def find_similar_jobs(request: JobRequest):
    try:
        logger.info(f"Nouvelle requête reçue pour le métier: {request.job_title}")
        
        # Chargement des données
        logger.info("Chargement des embeddings...")
        jobs_data = load_embeddings()
        logger.info("Données chargées avec succès")
        
        # Création de l'embedding
        logger.info("Création de l'embedding pour la requête...")
        input_embedding = model.encode(request.job_title)
        logger.info("Embedding créé avec succès")
        
        # Calcul des similarités
        logger.info("Calcul des similarités...")
        similarities = []
        
        for job_title, job_info in jobs_data.items():
            try:
                if "title_embedding" not in job_info:
                    logger.warning(f"Pas d'embedding trouvé pour {job_title}")
                    continue
                    
                title_embedding = job_info["title_embedding"]
                if not title_embedding:
                    logger.warning(f"Embedding vide pour {job_title}")
                    continue
                
                similarity = float(np.dot(input_embedding, title_embedding) / 
                                (np.linalg.norm(input_embedding) * np.linalg.norm(title_embedding)))
                
                skills = list(job_info.get("skills", {}).keys())
                similarities.append({
                    "job_title": job_title,
                    "similarity_score": similarity,
                    "skills": skills
                })
                
            except Exception as e:
                logger.error(f"Erreur lors du traitement de {job_title}: {str(e)}")
                continue
        
        if not similarities:
            logger.warning("Aucune similarité trouvée")
            raise HTTPException(
                status_code=404,
                detail="Aucun métier similaire trouvé"
            )
        
        # Tri et sélection des résultats
        similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
        top_results = similarities[:request.top_n]
        
        logger.info(f"Retour de {len(top_results)} résultats")
        return {
            "input_job": request.job_title,
            "similar_jobs": top_results
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la requête: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)