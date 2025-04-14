import os
from dotenv import load_dotenv

from src.steam_api import Steam
from data.steam_database import SteamDatabase
from src import logger


def main():
    load_dotenv()
    STEAM_API_KEY = os.getenv('STEAM_API_KEY')
    STEAM_USER_ID = os.getenv('STEAM_USER_ID')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    
    if not STEAM_API_KEY or not STEAM_USER_ID:
        raise ValueError("API keys must be set in environment variables")
    
    db = SteamDatabase('steam', 'postgres', DATABASE_PASSWORD)
    steam = Steam(STEAM_API_KEY, STEAM_USER_ID)
    user_data = steam.check_user_account()
    # if user has steam account add to database
    if user_data:
        db.add_steam_user(user_data)
        user_id = user_data['steamid']
    
        # check if wishlist for this user needs to be pulled from steam server
        is_wishlist_updated = db.check_update_status(user_id, 'wishlist_updated_at')
        
        wishlist = []
        print(is_wishlist_updated)
        if is_wishlist_updated:
            # call server to load and save wishlist
            wishlist = steam.get_wishlist()
            if wishlist:
                db.add_to_wishlist(user_id, wishlist)
        else:
            # call database to load wishlist
            wishlist = db.get_wishlist(user_id)
        
        # check if library for this user needs to be pulled from steam server
        is_library_updated = db.check_update_status(user_id, 'library_updated_at')
        
        library = []
        if is_library_updated:
            # call server to load and save library
            library = steam.get_library()
            if library:
                db.add_to_library(user_id, library)
        else:
            # call database to load library
            library = db.get_library(user_id)
        
        # logger.info(f"Library: \n{wishlist}")
    
if __name__ == '__main__':
    main()