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
API_ROOT_URL = os.getenv('API_ROOT_URL')
API_IA_ROOT_URL = f"http://{API_ROOT_URL}:{IA_API_PORT}"
API_DATA_ROOT_URL = f"http://{API_ROOT_URL}:{FASTAPI_PORT}"

API_IA_URL = API_IA_ROOT_URL + "/sentiment/"

st.title("Lire une citation")

mode = st.radio("Choisissez le mode de recherche:",
         ("Aléatoire", "Par ID "))

if mode == "Aléatoire":
    st.subheader("Citation Aléatoire")
    # afficher une citation aléatoire
    API_DATA_URL =  API_DATA_ROOT_URL + "/read/random/"
    if st.button("obtenir une citation aléatoire:"):
        try : 
            response = requests.get(API_DATA_URL)
            logger.info(f"Requete GET sur la route '/read/random/'")
            
            if response.status_code == 200:
                result = response.json()
                data = {'text': result.get('text', 'text non trouvé')}
                logger.info(f"Requete POST sur la route IA : '/sentiment/'")
                sentiment = requests.post(API_IA_URL, json=data)
                result_sentiment = sentiment.json()

                if result:
                    st.success(f"Citation avec ID {result.get('id', 'N/A')}")
                    logger.info(f"Citation avec ID {result.get('id', 'N/A')}")
                    st.info(result.get('text', 'text non trouvé'))
                    st.json(result_sentiment)
                    logger.info(f"Reponse des sentiments {result_sentiment}")
                    st.balloons()
                else:
                    st.warning("Aucune citation disponible dans la DB")
            else : 
                st.error(f"L'API a répondu avec une erreur : {response.status_code}")
                logger.error(f"L'API a répondu avec une erreur : {response.status_code}")
                st.write(response)


        except requests.exceptions.ConnectionError : 
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_DATA_URL}")
            logger.error(f"ERREUR : Impossible de se connecter à l'API à {API_DATA_URL}")
            st.warning("Veuillez vous assurer que le serveur est bien lancé en arrière plans")
            logger.error("Veuillez vous assurer que le serveur est bien lancé en arrière plans")

else:
    # afficher une citation par ID
    st.subheader("Citation par ID")
    API_DATA_URL =  API_DATA_ROOT_URL + "/read/"
    # selectionne l'ID
    # un formulaire
    with st.form("search_by_id"):
        quote_id = st.number_input("Entrez l'ID de la citation:", 
                                   min_value=1, step=1)
        submitted = st.form_submit_button("Rechercher")
    # connaitre toutes les id
    # selectionne l'id
    if submitted:
        # appel la route /read/id
        try : 
            response = requests.get(API_DATA_URL + str(quote_id) )
            logger.info(f"Requete GET sur la route '/read/{quote_id}'")
        # le reste est pareil
            if response.status_code == 200:
                result = response.json()
                data = {'text': result.get('text', 'text non trouvé')}
                logger.info(f"Requete POST sur la route IA : '/sentiment/'")
                sentiment = requests.post(API_IA_URL, json=data)
                result_sentiment = sentiment.json()

                if result:
                    st.success(f"Citation avec ID {quote_id}")
                    st.info(result.get('text', 'text non trouvé'))
                    logger.info(f"Citation avec ID {quote_id} : {result.get('text', 'text non trouvé')}")
                    st.json(result_sentiment)
                    logger.info(f"Reponse des sentiments {result_sentiment}")
                    st.balloons()

            elif response.status_code == 404:
                st.warning(f"La citation {quote_id} n'est pas disponible dans la DB")
                logger.warning(f"La citation {quote_id} n'est pas disponible dans la DB")
                    
            
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")
                logger.error(f"L'API a répondu avec une erreur : {response.status_code}")





        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_DATA_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")





