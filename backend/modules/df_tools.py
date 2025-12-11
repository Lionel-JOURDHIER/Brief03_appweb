import pandas as pd
import os
from loguru import logger

# configuration du log
logger.remove()
logger.add("backend/logs/database_api.log")

CSV_FILE_PATH = os.path.join("backend", "data", "quotes_db.csv")

def write_db (df : pd.DataFrame):
    """
    Write a csv file from a pandas DataFrame
    
    :param df: DataFrame with data you want to write in a file
    :type df: pd.DataFrame

    :returns: None
    """
    df.to_csv(
        path_or_buf=CSV_FILE_PATH,
        index=True,
        index_label= 'id',
        )
    logger.info(f"Ecriture de la base de données au format csv : {CSV_FILE_PATH}")

def read_db():
    """
    Read a csv file from the path CSV_FILE_PATH

    :returns: DataFrame with data you read from the file
    :type df: pd.DataFrame
    """
    df = pd.read_csv(
        filepath_or_buffer=CSV_FILE_PATH,
        index_col= 'id',
        )
    logger.info(f"Lecture de la base de données au format csv : {CSV_FILE_PATH}")
    logger.info(f"Création du DataFrame")
    df = check_df(df)
    return df

def initialise_db():
    """
    Write an empty csv file with 2 columns 'id' and 'text'

    """
    if os.path.exists(CSV_FILE_PATH):
        logger.info("La base de donnée existe")
    else : 
        logger.info(f"Impossible de trouver le fichier {CSV_FILE_PATH}")
        df = pd.DataFrame(columns=['id', 'text'])
        df = df.set_index('id')
        write_db(df)
        logger.info(f"le fichier {CSV_FILE_PATH} a été créé")

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
