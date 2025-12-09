# frontend/pages/0_inserer.py

import streamlit as st
import requests
import os
from dotenv import load_dotenv
from loguru import logger

# configuration du log
logger.remove()
logger.add("frontend/logs/streamlit.log")

load_dotenv()
IA_API_PORT = int(os.getenv('IA_API_PORT'))
FASTAPI_PORT = int(os.getenv('FASTAPI_PORT'))
API_ROOT_URL = os.getenv('API_ROOT_URL')
API_IA_ROOT_URL = f"http://{API_ROOT_URL}:{IA_API_PORT}"
API_DATA_ROOT_URL = f"http://{API_ROOT_URL}:{FASTAPI_PORT}"

API_DATA_URL = API_DATA_ROOT_URL + "/insert/"
API_IA_URL = API_IA_ROOT_URL + "/sentiment/"

st.title("Inserer une nouvelle citation")

with st.form("insert form"):
    new_quote_text = st.text_input("Texte de la citation :")
    submitted = st.form_submit_button("Ajouter la citation")
    if submitted : 
        data = {'text': new_quote_text}
        st.info("envoi à l'API")
    
        try:
            # 1. --- Requetes POST sur la route '/insert/' ---
            logger.info(f"Requete POST sur la route '/insert/'")
            reponse = requests.post(API_DATA_URL, json=data)
            logger.info(f"Requete POST sur la route IA : '/sentiment/'")
            sentiment = requests.post(API_IA_URL, json=data)
            if reponse.status_code == 200:
                # 2. --- Si il y a un resultat l'afficher ---
                result = reponse.json()
                result_sentiment = sentiment.json()
                st.success(f"Citation ajoutée ! ID: {result['id']} ")
                logger.info(f"Citation ajoutée ! ID: {result['id']} ")
                st.json(result)
                st.success(f"Votre citation à les sentiments suivants : ")
                st.json(result_sentiment)
                logger.info(f"Reponse des sentiments {result_sentiment}")
                st.balloons()
            else : 
                st.error(f"L'API a répondu avec une erreur : {reponse.status_code}")
                logger.error(f"L'API a répondu avec une erreur : {reponse.status_code}")

        except requests.exceptions.ConnectionError : 
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_DATA_URL}")
            logger.error(f"ERREUR : Impossible de se connecter à l'API à {API_DATA_URL}")
            st.warning("Veuillez vous assurer que le serveur est bien lancé en arrière plans")
            logger.error("Veuillez vous assurer que le serveur est bien lancé en arrière plans")


