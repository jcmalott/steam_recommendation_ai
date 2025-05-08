import os
from dotenv import load_dotenv
from transformers import AutoTokenizer

from src.store_to_db import StoreToDB
from src.steam_api import Steam
from data.steam_database import SteamDatabase

def load_game_data_to_db():
    game_finder = StoreToDB()
    has_steam_account = game_finder.load_user()
    
    if has_steam_account:
        game_finder.load_wishlist()
        game_finder.load_library()
        game_finder.store_game_data_to_db()
        game_finder.parse_payment_history() 

def main(load_game_data:bool = False):
    BASE_MODEL = "meta-llama/Meta-Llama-3.1-8B"
    load_dotenv()
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
    STEAM_API_KEY = os.getenv('STEAM_API_KEY')
    STEAM_USER_ID = os.getenv('STEAM_USER_ID')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    
    db = SteamDatabase('steam', 'postgres', DATABASE_PASSWORD)
    steam = Steam(STEAM_API_KEY, STEAM_USER_ID)
    
    user_games= []
    game_finder = StoreToDB(steam, db)
    wishlist = game_finder.load_wishlist(False)
    for game in wishlist:
        priority = game["priority"]
        user_games.append({
            "appid": game['appid'],
            # 0 means no priority set, 999 = user least interested in
            "priority": 999 if priority == 0 else priority,
            "playtime_minutes": 0,
            # -1 means user hasn't spent money on this item
            "user_paid_price": -1
        })
    library = game_finder.load_library(False)
    for game in library:
        # -1 means user hasn't spent money on this item
        user_paid_price = game["user_paid_price"] if game["user_paid_price"] else -1
        user_games.append({
            "appid": game['appid'],
            # if in library then user has the game, meaning they are highly interested = 1
            "priority": 1,
            "playtime_minutes": game['playtime_minutes'],
            "user_paid_price": user_paid_price
        })
    
    
    for user_game in user_games:
        appid = str(user_game["appid"])
        game_info = db.get_game(appid) 
        developers = db.get_developers(appid)
        categories = db.get_categories()
        new_data = {
            "game_name": game_info["game_name"],
            "is_free": game_info["is_free"],
            "detailed_description": game_info["detailed_description"],
            "recommendations": game_info["recommendations"],
            "esrb_rating": game_info["esrb_rating"],
            "developers": ",".join([developer for developer in developers["developer_name"]]),
            "categories": 
        }
        
        user_game = user_game | new_data
          

    # appid category_name
    categories = db.get_categories()
    publishers = db.get_publishers()
    genres = db.get_genres()
    prices = db.get_prices()
    # appid score
    metacritic = db.get_metacritics()
    # TODO: where does rating come from
    # rating, description
    # rating = db.get_rating()
        
    
    # All important info about a game
    # - use
    
    # tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    # tokenizer.encode(text, add_special_characters=False)

    # if load_game_data:
    #     load_game_data_to_db()
        
    # 
    
if __name__ == '__main__':
    main()