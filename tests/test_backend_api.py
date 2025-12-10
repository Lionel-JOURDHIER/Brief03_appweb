from fastapi.testclient import TestClient

# Si pas de pytest.ini : 
# import sys
# import os 

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app
from backend.API_IA.main import app_ia
from loguru import logger

# configuration du log
logger.remove()
logger.add("tests/logs/tests.log")

client = TestClient(app)

def test_root():
    response = client.get("/")
    test = response.status_code == 200
    if  test : 
        logger.info("Requete GET sur la route '/' : reussite")
    else : 
        logger.error("Requete GET sur la route '/' : echec")
    assert test

