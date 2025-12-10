#### Installation des biliothèque

`pip install fastapi uvicorn`

Un mini programme complet
* **Frontend**(streamlit)
  * **pages**
*  **backend**
  * **modules** (conntenir nos propres modules)
  * **data** (nos csv)

#### Architecture
```
mon_projet/
├── backend/                  
│   ├── __init__.py
│   ├── main.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── db_tools.py
│   │   └── df_tools.py
│   ├── API_IA/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── logs/
│   │       └── database_api.log
│   ├── logs/
│   │   └── database_api.log
│   └── data/
│       ├── quotes_db.db
│       └── quotes_db.csv
├── frontend/                 
│   ├── app.py
│   ├── logs/
│   │   └── streamlit.log
│   └── pages/
│       ├── 0_inserer.py
│       ├── 1_read.py
│       ├── 2_Rechercher.py
│       └── sentiment_streamlit.py
├── tests
│   ├── test_initiation.py
│   ├── test_backend_api.py
│   ├── test_backend_orm.py
│   └── logs/
│       └── tests.log
├── requirements.txt
├── README.md
├── .venv/
├── .env
└── .gitignore
```

#### Ma base de donnée "quotes_db.csv"
Columns : 
- `id`
- `text`

#### Commandes pour lancer le serveur uvicorn

`uvicorn chemin.nom:app --reload --log-level debug`

#### Comandes pour le terminal : 
pour power shell : 
Invoke-WebRequest -Methods GET "http://127.0.0.1:8000/"

pour linux 
curl -X GET "http://127.0.0.1:8000/"
