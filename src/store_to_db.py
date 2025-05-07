import os
from dotenv import load_dotenv
from tqdm import tqdm
import time
import json  

from src.steam_api import Steam
from data.steam_database import SteamDatabase
from src import logger
from src.tools.local_storage import check_file, load_from_json, save_to_json, remove_items, parse_library_purchase_history

class StoreToDB:
    load_dotenv()
    STEAM_API_KEY = os.getenv('STEAM_API_KEY')
    STEAM_USER_ID = os.getenv('STEAM_USER_ID')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    TEMP_FILE = 'data/temp_data.json'
    PAYMENT_HISTORY_FILE = 'data/payment_history.html'
    PAYMENT_HISTORY_DIR = 'data/purchase_history'
    BATCH_SIZE = 20 # items, How many resquests to make in one iteration
    # There is a 200 request limit every 5 mins. (5*60)/200 = 1.5
    SLEEP_TIME = 1.6 # Seconds, time between calling each game
    
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
            # TODO: only get new items and delete any removed ones, check db
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
            # TODO: only load new items to library, get items from db to check
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
        # only call if a week has passed from last mass update
        # are_games_updated = self.db.check_update_status(self.user_id, 'games_updated_at')
        # if not are_games_updated:
        #     return
    
        appids_to_download = []
        if check_file(self.TEMP_FILE):
            # load appid still to download
            appids_to_download = load_from_json(self.TEMP_FILE)["data"]
        else:
            # save all appids that need to be downloaded
            # appids_to_download = [item['appid'] for item in self.wishlist]
            appids_to_download = [item['appid'] for item in self.library]
            save_to_json(self.TEMP_FILE, appids_to_download)
        
        logger.info(f"Left to Download: {len(appids_to_download)}")  
        iterations = len(appids_to_download)
        ids_left = appids_to_download
        with tqdm(total=iterations, desc="Retrieving game data from server!", unit='game') as pbar:
            for i in range(0, iterations, self.BATCH_SIZE):
                batch_appids = appids_to_download[i:i+self.BATCH_SIZE]
                
                
                games_from_server = self.steam.get_games_data(batch_appids, self.SLEEP_TIME)
                # save games to DB
                
                # keep track of what appids still need to be downloaded
                # important incase there's an error while downloading
                ids_left = remove_items(ids_left, batch_appids)
                save_to_json(self.TEMP_FILE, ids_left)
                
                # save all game data to DB
                self.db.add_to_games(self.user_id, games_from_server)
                self.db.add_to_developers(self.user_id, games_from_server)
                self.db.add_to_publishers(self.user_id, games_from_server)
                self.db.add_to_categories(self.user_id, games_from_server)
                self.db.add_to_genres(self.user_id, games_from_server)
                self.db.add_to_prices(self.user_id, games_from_server)
                self.db.add_to_metacritic(self.user_id, games_from_server)
                # only sleep if there is still iterations to go
                pbar.update(iterations/self.BATCH_SIZE)
                
        self.db.set_games_update_status(self.user_id)
     
    def parse_payment_history(self, parse_data: bool = False):
        if parse_data:
            steam_purchase_history = parse_library_purchase_history(self.PAYMENT_HISTORY_DIR+"/steam")
            kinguin_purchase_history = parse_library_purchase_history(self.PAYMENT_HISTORY_DIR+"/kinguin")
            total_purchase_history = steam_purchase_history + kinguin_purchase_history
            save_to_json('data/purchase_names.json', total_purchase_history)
        orders = load_from_json('data/purchase_names.json')['data']
        self.db.add_paid_price(self.user_id, orders)