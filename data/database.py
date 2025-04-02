"""
    Connect to database and store data.
    * does every table need a primary key or can I just use a reference key
"""
import psycopg2 as pg2
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Database():
    
    def __init__(self, database: str, user: str, password: str):
        self.conn = pg2.connect(database=database, user=user, password=password)
        self.cur = self.conn.cursor()
    
    """ 
        - connect
        - store
        - 
    """
    def add_steam_user(self, user: Dict[str,Any]):
        is_user = self._check_steam_id(user['steamid'])
        if is_user:
            # user is already in db
            return None
        
        try:
            fields = ['steamid', 'persona_name', 'profile_url', 'avatar_full', 'real_name', 'country_code', 'state_code']
            columns = ', '.join(fields)
            placeholders = ', '.join(['%s'] * len(fields))

            query = f"""
                INSERT INTO users ({columns})
                VALUES ({placeholders})
            """
            self.cur.execute(query, [user[field] for field in fields])
            self.conn.commit()
            logger.info(f"DB - UserId {user['steamid']} has been created!")
        except pg2.Error as e:
            logger.error(f"ERROR: Database Insert User: {e}")
            if self.conn:
                self.conn.rollback()
        
    def add_to_wishlist(self, user_id: str, items: Dict[str, Any]) -> int:
        is_user = self._check_steam_id(user_id)
        if not is_user:
            return 0
            
        values = []
        try:
            query = "INSERT INTO wishlist (steamid, appid, priority) VALUES (%s, %s, %s) ON CONFLICT (steamid, appid) DO NOTHING"
            
            for item in items:
                if "appid" in item and "priority" in item:
                    values.append((user_id, item['appid'], item['priority']))
            
            self.cur.executemany(query, values)
            self.conn.commit()
        except pg2.Error as e:
            logger.error(f"ERROR: Database Insert Wishlist: {e}")
            if self.conn:
                self.conn.rollback()
                
        logger.info(f"Database: {len(values)} Items Added!")       
        return len(values)
    
    def _check_steam_id(self, user_id: str) -> bool:
        try:
            self.cur.execute(f"SELECT steamid FROM users WHERE steamid = '{user_id}'")
            if self.cur.fetchone() is not None:
                logger.info(f"Found User ID {user_id}!")
                return True
            else:
                logger.warning(f"DB User ID {user_id} doesn't exist!")
        except pg2.Error as e:
            logger.error(f"ERROR - Database Select User: {e}")
            
        return False