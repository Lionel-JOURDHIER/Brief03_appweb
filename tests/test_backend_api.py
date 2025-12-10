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

client2 = TestClient(app_ia)

def test_ia():
    test_sentiment_text = "congratulation"
    data = {'text': test_sentiment_text}
    response = client2.post("/sentiment/", json=data)
    test1 = response.status_code == 200
    if  test1 : 
        logger.info("Requete POST sur la route '/sentiment/' : reussite")
    else : 
        logger.error("Requete POST sur la route '/sentiment/' : echec")
    assert test1
    data_response = response.json()

    test2 = data_response == {
        "neg":0,
        "neu":0,
        "pos":1,
        "compound":0.5994
        }
    if  test2 : 
        logger.info("Verification des sentiments : reussite")
    else : 
        logger.error("Verification des sentiments : echec")
    assert test2
