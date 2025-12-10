# frontend/pages/0_insérer.py
import streamlit as st
import requests 
import os 
import pandas as pd
from dotenv import load_dotenv 
from loguru import logger

# configuration du log
logger.remove()
logger.add("frontend/logs/streamlit.log")

load_dotenv()

IA_API_PORT = int(os.getenv('IA_API_PORT'))
FASTAPI_PORT = int(os.getenv('FASTAPI_PORT'))
API_URL = os.getenv('API_ROOT_URL')
API_IA_ROOT_URL = f"http://{API_URL}:{IA_API_PORT}"
API_DATA_ROOT_URL = f"http://{API_URL}:{FASTAPI_PORT}"

st.title("Verifier un sentiment")

st.subheader("Entrer un texte pour vérifier son sentiment")
text_front = st.text

with st.form("insert form"):
    new_sentiment_text = st.text_input("Veuillez inserer le texte pour verifier les sentiments :")
    submitted = st.form_submit_button("Verifier les sentiments")
    if submitted : 
        data = {'text': new_sentiment_text}
        st.info("envoi à l'API")
        logger.info(f"Envoie du texte {new_sentiment_text} pour analyse")
        API_IA_URL =  API_IA_ROOT_URL + "/sentiment/"
        try:
            # 1. --- Requetes POST vers l'URL ---
            
            reponse = requests.post(API_IA_URL, json=data)
            logger.info(f"Requete POST sur la route IA : '/sentiment/'")
            if reponse.status_code == 200:
                # 2. --- Si il y a un resultat l'afficher ---
                result = reponse.json()
                st.success(f"Voici  les sentiments trouvés : ")
                st.json(result)
                logger.info(f"Reponse des sentiments {result}")
            elif reponse.status_code == 422:
                st.warning(f"Veuillez rentrer un texte dans le champ ")
                logger.warning("Field input_text : 'Veuillez inserer le texte pour verifier les sentiments :' submitted without value")
            else : 
                st.error(f"L'API a répondu avec une erreur : {reponse.status_code}")
                logger.error(f"L'API a répondu avec une erreur : {reponse.status_code}")

        except requests.exceptions.ConnectionError : 
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_IA_ROOT_URL}")
            logger.error(f"ERREUR : Impossible de se connecter à l'API à {API_IA_ROOT_URL}")
            st.warning("Veuillez vous assurer que le serveur est bien lancé en arrière plans")
            logger.error("Veuillez vous assurer que le serveur est bien lancé en arrière plans")