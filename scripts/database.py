import psycopg2
from sqlalchemy import create_engine
import os 
from typing import *
import pandas as pd

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

class DbConn:

    def __init__(self):
        self.conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
        
    
    def insert_data(self, Channel_Title, Channel_Username, ID, Message, Date, Media_Path):
        try:
            cur = self.conn.cursor()
            query = """
                INSERT INTO RawData (Channel_Title, Channel_Username, ID, Message, Date, Media_Path) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (Channel_Title, Channel_Username, ID, Message, Date, Media_Path))
            self.conn.commit()
            cur.close()
            self.conn.close()
        except Exception as e:
            print(f"Error: {e}")

    
    def read_data(self, table_name: str)-> List:
        '''
        This function is used to read data from a specific table

        Parameter:
        ---------
            table_name(str)

        Return:
        -------
            List: return a list of rows in the database
        '''

        cur = self.conn.cursor()
        cur.execute(f'SELECT * FROM "{table_name}"')
        rows = cur.fetchall()
        self.conn.close()
        return rows
    

class DatabaseConn:
    '''
    This class is for creating connection to the database and fetching data
    '''
    def __init__(self):      

        self.engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')

    def insert_dataframe_data(self, table_name: str, data: pd.DataFrame):
        '''
        This funtion saves dataframe to the database
        '''
        data.to_sql(table_name, self.engine, if_exists='replace')        
