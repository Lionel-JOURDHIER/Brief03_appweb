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
│   ├── logs/
│   │   └── database_api.log
│   └── data/
│       ├── quotes_db.db
│       └── quotes_db.csv
├── API_IA/
│   ├── __init__.py
│   ├── main.py
│   └── logs/
│       └── database_api.log
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

#### Comandes pour lancer l'API de la database : 
`python -m backend.main`
*old `python backend/main.py`*

#### Comandes pour lancer l'API de l'IA' : 
`python -m API_IA.main`
*old `python API_IA/main.py`*

#### Comandes pour lancer le front sur Streamlit' : 
`streamlit run frontend/app.py`


