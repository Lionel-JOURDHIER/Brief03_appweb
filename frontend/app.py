# frontend/app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from loguru import logger

# configuration du log
logger.remove()
logger.add("frontend/logs/streamlit.log")

load_dotenv()
API_PORT = int(os.getenv('FASTAPI_PORT'))
API_URL = os.getenv('API_ROOT_URL')
API_ROOT_URL = f"http://{API_URL}:{API_PORT}"

# pour des raisons de sécuritées. 
# il faut stocker cela comme variable d'environnement.

st.title("Démonstration d'API avec FastAPI et Streamlit")

st.subheader("verification de l'API")

# --- LE BOUTON ---
if st.button("ping l'API (Route /)"):
    try:
        # 1. --- Requetes GET  vers route principale ---
        reponse = requests.get(API_ROOT_URL)
        logger.info(f"Requete GET sur la route '/'")
        if reponse.status_code == 200:
            # 2. --- Si il y a un resultat l'afficher ---
            st.success(f"Connexion reussi à l'API FastAPI sur http://{API_URL}:{API_PORT} ! ")
            logger.info(f"Connexion reussi à l'API FastAPI sur http://{API_URL}:{API_PORT}")
            st.code(f"Statuts HTTP : {reponse.status_code}")
            st.json(reponse.json())
        else : 
            st.error(f"L'API a répondu avec une erreur : {reponse.status_code}")
            logger.error(f"L'API a répondu avec une erreur : {reponse.status_code}")

    except requests.exceptions.ConnectionError : 
        st.error(f"ERREUR : Impossible de se connecter à l'API à {API_ROOT_URL}")
        logger.error(f"ERREUR : Impossible de se connecter à l'API à {API_ROOT_URL}")
        st.warning("Veuillez vous assurer que le serveur est bien lancé en arrière plans")
        logger.error("Veuillez vous assurer que le serveur est bien lancé en arrière plans")


