"""
    Connect to database and store data.
    * does every table need a primary key or can I just use a reference key
"""
import psycopg2 as pg2

class Database():
    
    def __init__(self, database: str, user: str, password: str):
        conn = pg2.connect(database=database, user=user, password=password)
        cur = conn.cursor()
    
    """ 
        - connect
        - store
        - 
    """