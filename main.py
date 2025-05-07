from src.store_to_db import StoreToDB

def load_game_data_to_db():
    game_finder = StoreToDB()
    has_steam_account = game_finder.load_user()
    
    if has_steam_account:
        game_finder.load_wishlist()
        game_finder.load_library()
        game_finder.store_game_data_to_db()
        game_finder.parse_payment_history() 

def main(load_game_data:bool = False):
    if load_game_data:
        load_game_data_to_db()
        
    # 
    
if __name__ == '__main__':
    main()