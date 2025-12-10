# backend/main.py
import os
import uvicorn
import pandas as pd

from pydantic import BaseModel, Field
from fastapi import FastAPI
from dotenv import load_dotenv
from nltk.sentiment import SentimentIntensityAnalyzer
from loguru import logger

# configuration du log
logger.remove()
logger.add("backend/API_IA/logs/sentiment_api.log")

load_dotenv()

# modèles pydantic

# NonEmptyString = Annotated[str, StringConstraints(min_length=1)]

class SentimentRequest(BaseModel):
    #Verifie que le format soit conforme au modèle
    # text : NonEmptyString
    # text : str
    text : str = Field(min_length=1, description ="donner un texte pour verifier le sentiment")

class SentimentResponse(BaseModel):
    #Verifie que le format soit conforme au modèle
    neg : float
    neu : float
    pos : float
    compound : float

IA_API_PORT = int(os.getenv('IA_API_PORT'))
API_URL = os.getenv('API_ROOT_URL')
API_ROOT_URL = f"http://{API_URL}:{IA_API_PORT}"

# --- Configuration ---
app_ia = FastAPI(title="API_IA")

#décorateur s'applique à la fonction. 
# @app_ia.get("/")
# def read_root():
#     return {"Hello" : "World", "status" : "API is running"}

@app_ia.post("/sentiment/", response_model=SentimentResponse)
def verif_sentiment(sentiment : SentimentRequest):
    """
    check on the sentiment of an english phrase or word
    
    :param quote: Description
    :type quote: SentimentRequest
    """
    logger.info(f"Requete POST pour analyse de sentiments")
    #1 lancer le verificateur de sentiment
    sia = SentimentIntensityAnalyzer()
    #2 Recuperer le text du front
    text = sentiment.text
    logger.info(f"Reception du texte {text} pour analyse")
    #3 verifier le sentiment du text
    sentiment = sia.polarity_scores(text)
    #3 Faire un retour sur le front
    logger.info(f"Reponse des sentiments {sentiment}")
    return sentiment

if __name__ == "__main__" :
    print("Hello")
    # 1 on récupère le port de l'API
    try : 
        port = int(os.getenv('IA_API_PORT'))
        port = int(port)
        url = os.getenv('API_ROOT_URL')
        
    except ValueError :
        print("Erreur : IA_API_PORT invalide, utilisation du port par défaut 8000.")
        port = 8000
    logger.info(f"Démarrage du serveur FastAPI sur http://{url}:{port}")

    # 2. On lance uvicorn
    uvicorn.run(
        "backend.API_IA.main:app_ia",
        port = port,
        host = url,
        log_level="debug"
    )

