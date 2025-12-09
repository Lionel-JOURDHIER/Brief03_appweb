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
│   ├── main.py
│   ├── modules/
│   │   └── df_tools.py
│   └── data/
│       └── quotes_db.csv
├── frontend/                 
│   ├── app.py
│   └── pages/
│       ├──
│       ├──
│       └──
├── requirements.txt
├── README.md
├── .venv
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
