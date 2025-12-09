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

API_ROOT_URL =  f"http://{os.getenv('API_ROOT_URL')}:{os.getenv('FASTAPI_PORT', '8080')}"
API_URL =  API_ROOT_URL + "/read/"

st.title("Lire toutes les citations")

if st.button("Charger les données"):
    st.info("lire depuis l'API")

    try : 
        response = requests.get(API_URL)
        logger.info(f"Requete GET sur la route '/read/'")
        if response.status_code == 200:
            result = response.json()

            df = pd.DataFrame(result)
            st.dataframe(df, width="stretch")

            st.success("Lecture de toutes les citations")
            logger.info("Lecture de toutes les citations")
            st.balloons()
        else:
            st.error(f"Erreur de l'API avec le code {response.status_code}")
            logger.error(f"L'API a répondu avec une erreur : {response.status_code}")
            st.write(response)


    except requests.exceptions.ConnectionError : 
        st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
        logger.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
        st.warning("Veuillez vous assurer que le serveur est bien lancé en arrière plans")
        logger.error("Veuillez vous assurer que le serveur est bien lancé en arrière plans")
