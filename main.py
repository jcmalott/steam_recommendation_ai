import os
from dotenv import load_dotenv
from tqdm import tqdm
import time

from src.steam_api import Steam
from data.steam_database import SteamDatabase
from src import logger
from src.tools.local_storage import check_file, load_from_json, save_to_json, remove_items

class GameFinder:
    load_dotenv()
    STEAM_API_KEY = os.getenv('STEAM_API_KEY')
    STEAM_USER_ID = os.getenv('STEAM_USER_ID')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    TEMP_FILE = 'data/temp_data.json'
    BATCH_SIZE = 20 # items, How many resquests to make in one iteration
    # There is a 200 request limit every 5 mins. (5*60)/200 = 1.5
    SLEEP_TIME = 1.5 * BATCH_SIZE # Seconds, time between calling each game
    
    def __init__(self):
        if not self.STEAM_API_KEY or not self.STEAM_USER_ID:
            raise ValueError("API keys must be set in environment variables")
        self.db = SteamDatabase('steam', 'postgres', self.DATABASE_PASSWORD)
        self.steam = Steam(self.STEAM_API_KEY, self.STEAM_USER_ID)
        
    def load_user(self)-> bool:
        """
            Find user steam account from server. If one exist add their information to database.
            If no steam account nothing will happen.
            If user already in db nothing will happen.
            
            Return: True if user exist.
        """
        user_data = self.steam.check_user_account()
        if user_data:
            self.db.add_steam_user(user_data)
            self.user_id = user_data['steamid']
            
        return len(user_data) > 0
    
    def load_wishlist(self)-> bool:
        """
            Check db if user has a wishlist. If so was it added more than a week ago.
            If first time loading wishlist or last call has been under a week, then pull from steam server.
            If wishlist exist within db then pull from db.
            
            Return: True if wishlist was loaded.
            Note: User wishlist is updated every week to reduce overcalling server.
        """
        is_wishlist_updated = self.db.check_update_status(self.user_id, 'wishlist_updated_at')
        
        self.wishlist = []
        if is_wishlist_updated:
            # call server to load and save wishlist
            wishlist = self.steam.get_wishlist()
            if wishlist:
                self.db.add_to_wishlist(self.user_id, wishlist)
        else:
            # call database to load wishlist
            wishlist = self.db.get_wishlist(self.user_id)
        
        self.wishlist = wishlist    
        return len(self.wishlist) > 0
            
    def load_library(self)-> bool:
        """
            Check db if user has a library. If so was it added more than a week ago.
            If first time loading library or last call has been under a week, then pull from steam server.
            If library exist within db then pull from db.
            
            Return: True if library was loaded.
            Note: User library is updated every week to reduce overcalling server.
        """
        is_library_updated = self.db.check_update_status(self.user_id, 'library_updated_at')
        
        library = []
        if is_library_updated:
            # call server to load and save library
            library = self.steam.get_library()
            if library:
                self.db.add_to_library(self.user_id, library)
        else:
            # call database to load library
            library =self. db.get_library(self.user_id)
        
        self.library = library  
        return len(self.library) > 0
    
    def store_game_data_to_db(self):
        # self.library
        appids_to_download = []
        if check_file(self.TEMP_FILE):
            # load appid still to download
            appids_to_download = load_from_json(self.TEMP_FILE)["data"]
        else:
            # save all appids that need to be downloaded
            appids_to_download = [item['appid'] for item in self.wishlist]
            save_to_json(self.TEMP_FILE, appids_to_download)
        
        # TODO: best to just call a single game at a time and wait a sec inbetween
        # TODO: the server could timeout while a batch is taking place
        # TODO: why is the file not saving properly
        logger.info(f"Left to Download: {len(appids_to_download)}")  
        iterations = len(appids_to_download)
        with tqdm(total=iterations, desc="Retrieving game data from server!", unit='game') as pbar:
            for i in range(0, iterations, self.BATCH_SIZE):
                batch_appids = appids_to_download[i:i+self.BATCH_SIZE]
                
                games_from_server = self.steam.get_games_data(batch_appids)
                # save games to DB
                
                # keep track of what appids still need to be downloaded
                save_to_json(self.TEMP_FILE, remove_items(appids_to_download, batch_appids))
                self.db.add_to_games(self.user_id, games_from_server)
                self.db.add_to_developers(self.user_id, games_from_server)
                self.db.add_to_publishers(self.user_id, games_from_server)
                self.db.add_to_categories(self.user_id, games_from_server)
                self.db.add_to_genres(self.user_id, games_from_server)
                self.db.add_to_prices(self.user_id, games_from_server)
                self.db.add_to_metacritic(self.user_id, games_from_server)
                # only sleep if there is still iterations to go
                pbar.update(iterations/self.BATCH_SIZE)
                if i + self.BATCH_SIZE < iterations:
                    time.sleep(self.SLEEP_TIME)
                   
            
    
def main():
    game_finder = GameFinder()
    has_steam_account = game_finder.load_user()
    
    if has_steam_account:
        game_finder.load_wishlist()
        game_finder.load_library()
        game_finder.store_game_data_to_db()
    
if __name__ == '__main__':
    main()