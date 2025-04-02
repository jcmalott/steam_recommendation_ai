import os
from dotenv import load_dotenv
import logging

from src.steam_api import Steam
from data.database import Database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def main():
    load_dotenv()
    STEAM_API_KEY = os.getenv('STEAM_API_KEY')
    STEAM_USER_ID = os.getenv('STEAM_USER_ID')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    
    if not STEAM_API_KEY or not STEAM_USER_ID:
        raise ValueError("API keys must be set in environment variables")
    
    db = Database('steam', 'postgres', DATABASE_PASSWORD)
    
    steam = Steam(STEAM_API_KEY, STEAM_USER_ID)
    user_data = steam.get_user_data()
    # TODO check if user is in db, if not add them
    if user_data:
        db.add_steam_user(user_data)
    
    # wishlist = steam.get_wishlist()
    # logger.info(f"Wishlist: \n{wishlist}")
    
if __name__ == '__main__':
    main()