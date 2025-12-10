import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from loguru import logger

Base = declarative_base()

class Citations(Base):
    __tablename__ = 'citations'
    # clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)  
    text = Column(String, nullable=True)

DB_FILE_PATH = os.path.join("backend", "data", "quotes_db.db")
ENGINE = create_engine(f"sqlite:///{DB_FILE_PATH}", echo=True)

def create_session(engine = ENGINE):
    '''
    Create and return a new SQLAlchemy session.

    Args : 
        engine : sqlalchemy.Engine
            The SQLAlchemy engine connected to the database.

    Returns : 
        Session
            A new SQLAlchemy session instance.
    '''
    try : 
        # create the tables
        Base.metadata.create_all(engine)
        # open the session
        session = sessionmaker(bind=engine)
        return session()
    except Exception as e:
        print(f"Error creating database session: {e}")

def existing_citation():
    session = create_session()
    try :
        existing_citations = {
                p.text : p.id 
                for p in session.query(Citations).all()
            }
        return existing_citations
    finally : 
        session.close()

def write_db (df : pd.DataFrame):
    """
    Write a SQLLite file from a pandas DataFrame
    
    :param df: DataFrame with data you want to write in a file
    :type df: pd.DataFrame

    :returns: None
    """
    session = create_session()
    citations_to_add = []
    existing_citations = existing_citation()
    for _, row in df.iterrows():
        text = str(row['text'])
        if text in existing_citations :
            continue
        else : 
            citation = Citations(text=text)
            citations_to_add.append(citation)

    session.add_all(citations_to_add)

    session.commit()
    session.close()


def read_db():
    """
    Read a SQLLite file from the path DB_FILE_PATH

    :returns: DataFrame with data you read from the file
    :type df: pd.DataFrame
    """
    session = create_session()
    db = [
        {"id" : p.id , "text" : p.text}
        for p in session.query(Citations).all()
    ]
    if db == []:
        df = pd.DataFrame(columns=['id', 'text'])
        df = df.set_index('id')
    else :         
        df = pd.DataFrame(db)
        df = df.set_index('id')
        df = check_df(df)
    return df

def initialise_db():
    """
    Write an empty SQLLite file with 2 columns 'id' and 'text'
    """
    if os.path.exists(DB_FILE_PATH):
        logger.info("La base de donnée existe")
    else : 
        logger.info(f"Impossible de trouver le fichier {DB_FILE_PATH}")
        df = pd.DataFrame(columns=['id', 'text'])
        df = df.set_index('id')
        write_db(df)
        logger.info(f"le fichier {DB_FILE_PATH} a été créé")

def check_df(df: pd.DataFrame):
    """
    Read a dataframe
    :type df: pd.DataFrame
    :returns: DataFrame with empty rows filled with 'NULL' 
    """
    for index, row in df.iterrows() : 
        for col in df.columns:
            if pd.isna(row[col]):
                logger.info(f"NaN trouvé à la ligne {index}, colonne '{col}' remplacé par la valeur 'NULL'")
    df=df.fillna('NULL')
    write_db(df)
    return df
