import psycopg2 as pg2
from typing import Dict, Any, List
from src import logger

class SteamDatabase():
    """
        Database class to handle PostgreSQL connection and data operations for Steam Client
    """
    
    def __init__(self, database: str, user: str, password: str):
        """
            Initialize database connection
            
            Args:
                database: Name of the PostgreSQL database
                user: Database username
                password: Database password
        """
        self.conn = pg2.connect(database=database, user=user, password=password)
        # Allows enteraction with database
        self.cur = self.conn.cursor()

    def add_steam_user(self, user: Dict[str,Any]) -> bool:
        """
            Add Steam user to database if not already present
            
            Args:
                user: Dictionary containing Steam user account data
                
            Returns: bool, False if user already exist
        """
        # checking to see if user exist, if so exit
        is_user = self._check_table_item('steamid','users', user['steamid'])
        if is_user:
            # user is already in db
            return False
        
        # fields within the database to be populated
        fields = ['steamid', 'persona_name', 'profile_url', 'avatar_full', 'real_name', 'country_code', 'state_code']
        self._insert_new_row('users', fields, [user])
        return True
        
    def add_to_wishlist(self, user_id: str, items: List[Dict[str, Any]]) -> int:
        is_user = self._check_table_item('steamid','users',user_id)
        if not is_user:
            return 0
        
        # if wishlist item is already in DB then just update priority level
        on_conflict = f"""
            ON CONFLICT (steamid, appid)
            DO UPDATE SET
                priority = EXCLUDED.priority
        """   
        has_passed = self._insert_new_row('wishlist', ['steamid', 'appid', 'priority'], items, on_conflict)
        if has_passed:
            logger.info(f"DB - Wishlist - Total Items {len(items)} have been added!")     
        return len(items)
    
    def get_wishlist(self, user_id: str)-> List[Dict[str,Any]]:
        fields = ['steamid', 'appid', 'priority']
        return self._search_db(user_id, fields, 'wishlist')
    
    def add_to_library(self, user_id: str, items: List[Dict[str, Any]]):
        is_user = self._check_table_item('steamid','users', user_id)
        if not is_user:
            return 0
        
        on_conflict = f"""
            ON CONFLICT (steamid, appid)
            DO UPDATE SET
                playtime_minutes = EXCLUDED.playtime_minutes
        """   
        has_passed = self._insert_new_row('user_library', ['steamid', 'appid', 'playtime_minutes'], items, on_conflict)
        if has_passed:
            logger.info(f"DB - Library - Total Items {len(items)} have been added!")     
        return len(items)
        
    def get_library(self, user_id: str)-> List[Dict[str,Any]]:
        fields = ['steamid', 'appid', 'playtime_minutes']
        return self._search_db(user_id, fields, 'user_library')
    
    def _search_db(self, user_id: str, fields: List[str], table: str)-> List[Dict[str,Any]]:
        is_user = self._check_table_item('steamid','users', user_id)
        if is_user:
            try:
                columns = ', '.join(fields)
                # gets users wishlist
                query = f"""
                    SELECT {columns} FROM {table}
                    WHERE steamid = '{user_id}';
                """
                
                self.cur.execute(query)
                items = self.cur.fetchall()
                
                # need to return in json format just like the server would
                items_dict = []
                for item in items:
                    item_json = {}
                    for index,field in enumerate(fields):
                        item_json[field] = item[index]
                    
                    items_dict.append(item_json) 
                
                logger.info(f"Database {table} {len(items_dict)} Fetched")
                return items_dict
            except pg2.Error as e:
                logger.error(f"ERROR: Database Fetching {table}: {e}")
                if self.conn:
                    self.conn.rollback()
                
        return []  
    
    def check_update_status(self, user_id: str, column: str) -> bool:
        """
            Check if data needs to be called down from server or retrieved from database.
            A lot of calls to the server are needed to download wishlist and library game data.
            For this a week interval is set between download new data
            
            Args:
                user_id: Steam user ID
                column: Name of the column to check when last updated
                
            Returns: bool, True if data needs to be updated
        """
        # check if user has stored data already
        is_user = self._check_table_item('steamid', 'schedule_data_retrieval', user_id)
        # if no user than schedule update
        if is_user:
            try:
                # checks if a week has passed since last update
                query = f"""
                    SELECT needs_retrieval({column}) 
                    FROM schedule_data_retrieval 
                    WHERE steamid = '{user_id}';
                """
                
                self.cur.execute(query)
                first_item = self.cur.fetchone()
                # sometimes it gets return as a single item or tuple, even when its just one item
                first_item = first_item[0] if isinstance(first_item, tuple) else first_item
                return first_item
            except pg2.Error as e:
                logger.error(f"ERROR: Database Fetching Schedule: {e}")
                if self.conn:
                    self.conn.rollback()
                    
        return True
    
    def _insert_new_row(self, table: str, fields: List[str], items: List[Dict[str, Any]], on_conflict: str='') -> bool:
        """
            Insert a new row into specified table
            Each field corresponds to a key within items
            
            Args:
                table: Name of the table to insert into
                fields: List of column names for values to be placed
                items: values to place within each field
            Return: True is row was inserted, otherwise False
        """
        try:
            columns = ', '.join(fields)
            placeholders = ', '.join(['%s'] * len(fields))

            query = f"""
                INSERT INTO {table} ({columns})
                VALUES ({placeholders})
            """
            query += on_conflict
            
            values = []
            for item in items:
                row_values = [item[field] for field in fields]
                values.append(row_values)
                
            # place all item values in placeholder spot, then execute query
            self.cur.executemany(query, values)
            self.conn.commit()
            return True
        except pg2.Error as e:
            logger.error(f"ERROR: Database Insert {table}: {e}")
            if self.conn:
                self.conn.rollback()
                
        return False
            
    def _check_table_item(self, column: str, table: str, item) -> bool:
        """
            Check if an item exists in a specific column of a table
            
            Args:
                column: Column name to check
                table: Table name to check
                item: Value to search for
                
            Returns: bool, indicating if item exists
        """
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