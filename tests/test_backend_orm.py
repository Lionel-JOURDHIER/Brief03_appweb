import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd

from loguru import logger
# configuration du log
logger.remove()
logger.add("backend/logs/database_api.log")

from backend.modules.db_tools import write_db, read_db, initialise_db, Base, Citations

# ---------------
# --- FIXTURE ---
# ---------------
## create engine
@pytest.fixture(scope="module")
def engine_test():
    """Create engine"""
    return create_engine("sqlite:///:memory:")

## create DB
@pytest.fixture(scope="module")
def setup_db(engine_test):
    """Create table"""
    Base.metadata.create_all(engine_test)
    yield 
    Base.metadata.drop_all(engine_test)

## create DB session
@pytest.fixture(scope="function")
def db_session(engine_test,setup_db):
    """Yield DB Session"""
    connection = engine_test.connect()
    transaction = connection.begin()

    SessionTest = sessionmaker(autocommit = False, autoflush = False, bind=engine_test)
    session = SessionTest(bind=connection)

    yield session

    #clean
    session.close()
    transaction.rollback()
    connection.close()

## create DF

# ------------
# --- MOCK ---
# ------------
## override Session Locale
@pytest.fixture(autouse=True)
def override_create_session(monkeypatch,db_session):
    """Mock create_session"""
    def mock_create_session():
        return db_session
    monkeypatch.setattr('backend.modules.db_tools.create_session', mock_create_session)

# ------------
# --- TEST ---
# ------------

def test_add_and_read_citations():
    quote = "test"
    dico = [{"text" : quote}]
    df = pd.DataFrame(dico)
    # add citation
    write_db(df)
    #read citation
    df2 = read_db()
    citation = df2.iloc[0]['text']
    assert quote == citation

