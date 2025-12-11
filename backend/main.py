# backend/main.py
import os
import uvicorn
import pandas as pd
import random
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from typing import List
from loguru import logger

#! from modules.db_tools import write_db, read_db, initialise_db
from backend.modules.db_tools import write_db, read_db, initialise_db

# configuration du log
logger.remove()
logger.add("backend/logs/database_api.log")

load_dotenv()

# modèles pydantic

# NonEmptyString = Annotated[str, StringConstraints(min_length=1)]

class QuoteRequest(BaseModel):
    #Verifie que le format soit conforme au modèle
    # text : NonEmptyString
    # text : str
    text : str = Field(min_length=1, description ="donner un texte pour la citation")

class QuoteResponse(BaseModel):
    #Verifie que le format soit conforme au modèle
    id : int
    text : str

initialise_db()

API_PORT = int(os.getenv('FASTAPI_PORT'))
API_URL = os.getenv('API_ROOT_URL')
API_ROOT_URL = f"http://{API_URL}:{API_PORT}"

# --- Configuration ---
app = FastAPI(title="API")

# --- Routes API --- 
# http: /www.google.com/fr : route fr
# http: /www.google.com/en : route en
# http: /www.google.com : route principale

#décorateur s'applique à la fonction. 
@app.get("/")
def read_root():
    logger.info(f"Requete GET sur la route '/'")
    return {"Hello" : "World", "status" : "API is running"}

@app.post("/insert/", response_model=QuoteResponse)
def insert_quote(quote : QuoteRequest):
    """
    Insert une nouvelle citation
    
    :param quote: Description
    :type quote: QuoteRequest
    """
    logger.info(f"Requete POST sur la route '/insert/'") 
    # 1. trouver de dernier id du csv
    df = read_db()
    # 2. donner un id à sa citation
    if df.empty : 
        new_id = 1
    elif df.index.max() <= 0:
        new_id = 1
    else : 
        # pour le cas CSV
        new_id = 1 + df.index.max() 
    logger.info(f"Creation de l'id : {new_id} pour le stockage de la citation'") 
    # 3. enregister le fichier csv
    # Verifier que le texte n'est pas vide
    #3.1 création d'une nouvelle ligne
    objet = {"text" : [quote.text]}
    logger.info(f"Creation de l'objet et récupération de la citation {quote.text}")
    new_row = pd.DataFrame(objet, index = [new_id])

    #3.2 enregistrer le fichier csv
    df = pd.concat([df, new_row])
    logger.info(f"Ecriture de la base de donnée")
    write_db(df)

    # 4. envoi à l'app la citation avec id 
    logger.info(f"Envoie à l'app du QuoteResponse : {int(new_id), quote.text}")
    return {'id':new_id, 'text':quote.text}

@app.get("/read/", response_model=List[QuoteResponse])
def read_all_quotes():
    logger.info(f"Requete GET sur la route '/read/'")
    logger.info(f"Lecture de la base de donnée")
    df = read_db()
    logger.info(f"Envoi de la reponse List[QuoteResponse]")
    return df.reset_index().rename(columns={'id':'id','text':'text'}).to_dict('records')

@app.get("/read/{id}", response_model=QuoteResponse)
def read_specific_quotes(id : int):
    # il me faut toutes les citations pour les connaitres
    logger.info(f"Requete GET sur la route '/read/{id}'")
    logger.info(f"Lecture de la base de donnée")
    df = read_db()
    # filtre par l'id concerné
    logger.info(f"Filtrage la base de donnée par l'id : {id}")
    if id not in df.index:
        logger.warning(f"Citation avec ID {id} non trouvée")
        raise HTTPException(status_code=404, detail=f"Citation avec ID {id} non trouvée")
    quote_data = df.loc[id].to_dict()
    quote_data['id'] = id
    # retourne les résultats
    logger.info(f"Envoi de la reponse QuoteResponse : {quote_data}")
    return quote_data

@app.get("/read/random/", response_model=QuoteResponse)
def read_random_quotes():
    logger.info(f"Requete GET sur la route '/read/random/'")
    # il me faut toutes les citations pour les connaitres
    logger.info(f"Lecture de la base de donnée")
    df = read_db()
    # filtre par l'id concerné  
    if df.empty:
        logger.warning(f"la base de donnée est vide")
        raise HTTPException(status_code=404, detail=f"Citation avec aléatoire non trouvée")
    random_id = random.choice(df.index)
    logger.info(f"choix de l'index aléatoire : {random_id}")
    quote_data = df.loc[random_id].to_dict()
    quote_data['id'] = random_id
    # retourne les résultats
    logger.info(f"Envoi de la reponse QuoteResponse : {quote_data}")
    return quote_data

if __name__ == "__main__" :
    print("Hello")
    # 1 on récupère le port de l'API
    try : 
        port = int(os.getenv('FASTAPI_PORT'))
        port = int(port)
        url = os.getenv('API_ROOT_URL')
        
    except ValueError :
        print("Erreur : FASTAPI_PORT invalide, utilisation du port par défaut 8000.")
        port = 8000

    logger.info(f"Démarrage du serveur FastAPI sur http://{url}:{port}")

    # 2. On lance uvicorn
    uvicorn.run(
        #! "main:app",
        "backend.main:app",
        port = port,
        host = url,
        log_level="debug"
    )


