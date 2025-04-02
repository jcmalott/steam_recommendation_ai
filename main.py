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
    
    database = Database('', 'postgres', DATABASE_PASSWORD)
    
    steam = Steam(STEAM_API_KEY, STEAM_USER_ID)
    wishlist = steam.get_wishlist()
    logger.info(f"Wishlist: \n{wishlist}")
    
if __name__ == '__main__':
    main()