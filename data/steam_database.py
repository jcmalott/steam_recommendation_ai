import psycopg2 as pg2
from typing import Dict, Any, List
from src import logger

from src.tools.local_storage import remove_items

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
        # remove items no longer in wishlist
        stored_wishlist = self.get_wishlist(user_id)
        stored_appids = [item['appid'] for item in stored_wishlist]
        new_appids = [item['appid'] for item in items]
        
        appids_to_delete = remove_items(stored_appids, new_appids)
        self._delete_entries(user_id, 'wishlist', appids_to_delete)
        
        on_conflict = f"""
            ON CONFLICT (steamid, appid)
            DO UPDATE SET
            priority = EXCLUDED.priority
        """ 
        fields = ['steamid', 'appid', 'priority']
        table = 'wishlist'
        return self._add_to_database(user_id, items, on_conflict, fields, table)
    
    def get_wishlist(self, user_id: str)-> List[Dict[str,Any]]:
        fields = ['steamid', 'appid', 'priority']
        return self._search_db(user_id, fields, 'wishlist')
    
    def add_to_library(self, user_id: str, items: List[Dict[str, Any]]):
        on_conflict = f"""
            ON CONFLICT (steamid, appid)
            DO UPDATE SET
                playtime_minutes = EXCLUDED.playtime_minutes
        """   
        fields = ['steamid', 'appid', 'playtime_minutes']
        table = 'user_library'
        return self._add_to_database(user_id, items, on_conflict, fields, table)
        
    def get_library(self, user_id: str)-> List[Dict[str,Any]]:
        fields = ['steamid', 'appid', 'playtime_minutes']
        return self._search_db(user_id, fields, 'user_library')
    
    def add_to_games(self, user_id: str, items: List[Dict[str, Any]]):
        on_conflict = f"""
            ON CONFLICT (appid)
            DO UPDATE SET
                is_free = EXCLUDED.is_free,
                recommendations = EXCLUDED.recommendations
        """   
        fields = ['appid','game_type', 'game_name', 'is_free', 'detailed_description','header_image','website','recommendations','release_date','esrb_rating']
        table = 'games'
        return self._add_to_database(user_id, items, on_conflict, fields, table)
    
    
    def get_games(self, user_id: str)-> List[Dict[str,Any]]:
        fields = ['appid','game_type', 'game_name', 'is_free', 'detailed_description','header_image','website','recommendations','release_date','esrb_rating']
        return self._search_db(user_id, fields, 'games')
    
    def add_to_developers(self, user_id: str, items: List[Dict[str, Any]])-> int:
        on_conflict = f"""
            ON CONFLICT (appid, developer_name)
            DO NOTHING
        """   
        fields = ['appid','developer_name']
        table = 'developers'
        return self._add_to_database(user_id, items, on_conflict, fields, table)
    
    def get_developers(self, user_id: str)-> List[Dict[str,Any]]:
        fields = ['appid','developer_name']
        return self._search_db(user_id, fields, 'developers')
    
    def add_to_publishers(self, user_id: str, items: List[Dict[str, Any]])-> int:
        on_conflict = f"""
            ON CONFLICT (appid, publisher_name)
            DO NOTHING
        """   
        fields = ['appid','publisher_name']
        table = 'publishers'
        return self._add_to_database(user_id, items, on_conflict, fields, table)
    
    def get_publishers(self, user_id: str)-> List[Dict[str,Any]]:
        fields = ['appid','publisher_name']
        return self._search_db(user_id, fields, 'publishers')
    
    def add_to_categories(self, user_id: str, items: List[Dict[str, Any]]):
        on_conflict = f"""
            ON CONFLICT (appid, category_name)
            DO NOTHING
        """   
        fields = ['appid','category_name']
        table = 'categories'
        return self._add_to_database(user_id, items, on_conflict, fields, table)
    
    def get_categories(self, user_id: str):
        fields = ['appid','category_name']
        return self._search_db(user_id, fields, 'categories')
    
    def add_to_genres(self, user_id: str, items: List[Dict[str, Any]]):
        on_conflict = f"""
            ON CONFLICT (appid, genre_name)
            DO NOTHING
        """   
        fields = ['appid','genre_name']
        table = 'genres'
        return self._add_to_database(user_id, items, on_conflict, fields, table)
    
    def get_genres(self, user_id: str):
        fields = ['appid','genre_name']
        return self._search_db(user_id, fields, 'genres')
    
    def add_to_prices(self, user_id: str, items: List[Dict[str, Any]]):
        on_conflict = f"""
            ON CONFLICT (appid)
            DO UPDATE SET
                currency = EXCLUDED.currency,
                price_in_cents = EXCLUDED.price_in_cents,
                final_formatted = EXCLUDED.final_formatted,
                discount_percentage = EXCLUDED.discount_percentage
        """  
        fields = ['appid','currency','price_in_cents','final_formatted','discount_percentage']
        table = 'prices'
        return self._add_to_database(user_id, items, on_conflict, fields, table)
    
    def get_prices(self, user_id: str):
        fields = ['appid','currency','price_in_cents','final_formatted','discount_percentage']
        return self._search_db(user_id, fields, 'prices')
    
    def add_to_metacritic(self, user_id: str, items: List[Dict[str, Any]]):
        on_conflict = f"""
            ON CONFLICT (appid)
            DO UPDATE SET
                score = EXCLUDED.score
        """   
        fields = ['appid','score','url']
        table = 'metacritic'
        return self._add_to_database(user_id, items, on_conflict, fields, table)
    
    def get_metacritics(self, user_id: str):
        fields = ['appid','score','url']
        return self._search_db(user_id, fields, 'metacritic')
    
    def _add_to_database(self, user_id: str, items: List[Dict[str, Any]], on_conflict: str, fields: List, table: str)-> int:
        is_user = self._check_table_item('steamid','users', user_id)
        if not is_user:
            return 0
        
        has_passed = self._insert_new_row(table, fields, items, on_conflict)
        if has_passed:
            logger.info(f"DB - {table} - Total Items {len(items)} have been added!")     
        return len(items)
    
    def _search_db(self, user_id: str, fields: List[str], table: str)-> List[Dict[str,Any]]:
        try:
            columns = ', '.join(fields)
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
    
    def _delete_entries(self, user_id: str, table: str, items: List[Any]) -> bool:
        """
            Delete all entries of user from specified table
            
            user_id: User id that correspondes to steamid from table 
            table: Name of the table to delete from
            Return: True if entries delete, otherwise False
        """
        try:
            appids = ', '.join(items)
            query = f"""
                DELETE FROM {table}
                WHERE steamid = '{user_id}' AND appid IN ({appids})
            """
                
            # place all item values in placeholder spot, then execute query
            self.cur.execute(query)
            self.conn.commit()
            logger.info(f"Database SteamID {user_id}, DELETE {len(items)} items from {table}")
            return True
        except pg2.Error as e:
            logger.error(f"ERROR: Database DELETE {table}: {e}")
            if self.conn:
                self.conn.rollback()
                
        return False
    
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