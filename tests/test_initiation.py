from loguru import logger
from pytest import approx

# configuration du log
logger.remove()
logger.add("tests/logs/tests.log")

# assert condition  retoure une erreur si la condition est fausse. 
# assert 0 == 0 --> OK 
# assert 0 == 1 --> pas ok

GLOBAL = 1.256

def test_bidon():
    logger.info("test de réussite sur nombres")
    tests = []
    test_1 = 1 == 1.0
    tests.append(test_1)
    test_2 = 0 == 0
    tests.append(test_1)
    if all(test for test in tests) :
        logger.info("test de réussite sur nombres : reussite")
    else : 
        logger.error("test de réussite sur nombres : echec")
    assert test_1
    assert test_2

def test_bidon2():
    logger.info("test de erreur sur nombres")
    test = 0 == 0
    if  test : 
        logger.info("test de erreur sur nombres : reussite")
    else : 
        logger.error("test de erreur sur nombres : echec")
    assert test

def test_bidon3():
    logger.info("test de reussite sur str")
    condition = "a" == "a"
    if  condition : 
        logger.info("test de reussite sur str : reussite")
    else : 
        logger.error("test de reussite sur str : echec")
    assert condition

def test_bidon4():
    logger.info("test de Variables GLOBALE")
    test = GLOBAL > 1
    if  test : 
        logger.info("test de Variables GLOBAL : reussite")
    else : 
        logger.error("test de Variables GLOBAL : echec")
    assert test

def test_bidon5():
    logger.info("test de fonction approx : 10**-6")
    test = approx(1.0000001) == 1
    if  test : 
        logger.info("test de fonction approx : reussite")
    else : 
        logger.error("test de fonction approx : echec")
    assert test

#! test unitaire : un test par fonctionnalité
#! test intégration : ensemble de tout les test d'une API. 