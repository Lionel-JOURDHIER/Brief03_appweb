# frontend/pages/0_inserer.py

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_PORT = int(os.getenv('FASTAPI_PORT'))
API_URL = os.getenv('API_ROOT_URL')
API_ROOT_URL = f"http://{API_URL}:{API_PORT}"

API_URL = API_ROOT_URL + "/insert"

st.title("Inserer une nouvelle citation")

with st.form("insert form"):
    new_quote_text = st.text_input("Texte de la citation :")
    submitted = st.form_submit_button("Ajouter la citation")
    if submitted : 
        data = {'text': new_quote_text}
        st.info("envoi à l'API")
    
        try:
            # 1. --- Requetes GET  vers route principale ---
            reponse = requests.post(API_URL, json=data)
            if reponse.status_code == 200:
                # 2. --- Si il y a un resultat l'afficher ---
                result = reponse.json()
                st.success(f"Citation ajoutée ! ID: {result['id']} ")
                st.json(result)
                st.balloons()
            else : 
                st.error(f"L'API a répondu avec une erreur : {reponse.status_code}")

        except requests.exceptions.ConnectionError : 
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur est bien lancé en arrière plans")


