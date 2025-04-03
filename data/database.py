"""
    Connect to database and store data.
    * does every table need a primary key or can I just use a reference key
"""
import psycopg2 as pg2
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Database():
    
    def __init__(self, database: str, user: str, password: str):
        self.conn = pg2.connect(database=database, user=user, password=password)
        self.cur = self.conn.cursor()

    def add_steam_user(self, user: Dict[str,Any]):
        is_user = self._check_table_item('steamid','users', user['steamid'])
        if is_user:
            # user is already in db
            return None
        
        fields = ['steamid', 'persona_name', 'profile_url', 'avatar_full', 'real_name', 'country_code', 'state_code']
        self._insert_new_row('users', fields, user)
        
    def add_to_wishlist(self, user_id: str, items: Dict[str, Any]) -> int:
        # ON CONFLICT (steamid, appid) DO NOTHING
        is_user = self._check_table_item('steamid','users',user_id)
        if not is_user:
            return 0
            
        values = []
        self._insert_new_row('wishlist', ['steamid', 'appid', 'priority'], items)
        logger.info(f"DB - Wishlist - Total Items {len(items)} have been added!")     
        return len(values)
    
    def check_update_status(self, user_id: str, column: str) -> bool:
        is_user = self._check_table_item('steamid','schedule_data_retrieval', user_id)
        # if no schedule is being tracked for that user, then data needs to be updated
        if not is_user:
            return False
        
        try:
            query = f"""
                SELECT needs_retrieval({column}) 
                FROM schedule_data_retrieval 
                WHERE steamid = '{user_id}';
            """
            
            self.cur.execute(query)
            return self.cur.fetchone()
        except pg2.Error as e:
            logger.error(f"ERROR: Database Fetching Schedule: {e}")
            if self.conn:
                self.conn.rollback()
    
    def _insert_new_row(self, table: str, fields: List[str], items: Dict[str, Any]):
        try:
            columns = ', '.join(fields)
            placeholders = ', '.join(['%s'] * len(fields))

            query = f"""
                INSERT INTO {table} ({columns})
                VALUES ({placeholders})
            """
            self.cur.execute(query, [items[field] for field in fields])
            self.conn.commit()
        except pg2.Error as e:
            logger.error(f"ERROR: Database Insert {table}: {e}")
            if self.conn:
                self.conn.rollback()
            
    def _check_table_item(self, column: str, table: str, item) -> bool:
        try:
            self.cur.execute(f"SELECT {column} FROM {table} WHERE {column} = '{item}'")
            if self.cur.fetchone() is not None:
                logger.info(f"Found - Item: {item}, From Table: {table} Column {column}!")
                return True
            else:
                logger.warning(f"Doesn't Exist - Item: {item}, From Table: {table} Column {column}!")
        except pg2.Error as e:
            logger.error(f"ERROR - Database Selection: {e}")
            
        return False