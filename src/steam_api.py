""" 
    Helpful Links:
    https://api.steampowered.com/IWishlistService/GetWishlist/v1?steamid=76561198041511379
    Wishlist
    
    https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=09A19535C0064A3301527FD3AE352D7E&steamid=76561198041511379&format=json&include_played_free_games=True
    In Library
    
    https://store.steampowered.com/api/appdetails?appids=532790
    Game Info
"""
import requests
from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Steam():
    """ 
     Steam API client class to access data.
     - User wishlist and library
     - Game data
     - Steam user accounts
    """
    # URL endpoints for different Steam API services
    STEAM_WISHLIST_URL = 'https://api.steampowered.com/IWishlistService/GetWishlist/v1'
    STEAM_LIBRARY_URL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    STEAM_GAME_URL = 'https://store.steampowered.com/api/appdetails'
    STEAM_USER_URL = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    
    def __init__(self, steam_api_key: str, user_id: str):
        """ 
            Initialize Steam API client with API key and user ID
            
            Args:
                steam_api_key: Steam API key for authentication
                user_id: Steam user ID to retrieve data for
        """
        self.steam_api_key = steam_api_key
        self.user_id = user_id
        # Immediately fetch user data on initialization
        self.user = self._get_steam_user_data()
        
    # def get_wishlist(self) -> List[str]:
    #     """ 
    #         * When updating a wishlist you will need to delete and add wishlist items stored in database
    #     """
    #     user_id = self.user['steamid']
    #     params = {
    #         'key': self.steam_api_key,
    #         'steamid': user_id
    #     }
        
    #     try:
    #         logger.info(f"Steam Wishlist URL: {self.STEAM_WISHLIST_URL}?key={params['key']}&steamid={params['steamid']}")
    #         response = requests.get(self.STEAM_WISHLIST_URL, params=params)
    #         response.raise_for_status()
            
    #         data = self._process_wishlist_data(response.json())
    #         # save data to database
    #         # only download this data once a day
    #         # TODO do use db here
    #         # db.add_to_wishlist(user_id, data)
    #         if not data:
    #             logger.warning(f"UserId: {user_id} has no wishlist items!")
                
    #         return data
    #     except requests.RequestException as e:
    #         logger.error(f"Failed to retrieve wishlist from UserId {user_id}!")
        
    # def get_library(self):
    #     """ 
    #     """
    #     params = {
    #         'key': self.steam_api_key,
    #         'steamid': self.user['steamid'],
    #         'format': 'json',
    #         'include_played_free_games': True
    #     }
        
    #     data = self._process_library_data()
        
    # def get_game_data(self, appid):
    #     """ 
    #     """
    #     params = {
    #         'appids': appid
    #     }
        
    #     self._process_game_data(appid)
        
    def get_user_data(self) -> Dict[str, Any]:
        """
            Returns a users steam account information.
            
            Returns:
                Dictionary containing user account information
        """
        return self.user
        
    def _get_steam_user_data(self) -> Dict[str, Any]:
        """
            Retrieves a user steam account information.
                
            Returns:
                Dictionary containing user profile information or empty dict if user not found
        """
        params = {
            'key': self.steam_api_key,
            'steamids': self.user_id
        }
        
        try:
            logger.info(f"Steam User URL: {self.STEAM_USER_URL}?key={params['key']}&steamids={params['steamids']}")
            response = requests.get(self.STEAM_USER_URL, params=params)
            response.raise_for_status()
            
            # only store profile data that is needed
            data = self._process_user_data(response.json())
            
            if not data:
                logger.warning(f"Steam UserId: {self.user_id} doesn't exist!")
                # TODO throw exception for user not found
            
            return data
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve UserId {self.user_id}!")
            raise ValueError(f"Failed to retrieve UserId {self.user_id}!")
            
    def _process_user_data(self, response: Dict[str,Any]) -> Dict[str, Any]:
        """ 
            Process users Steam account data
            
            Args:
                response: JSON response containing Steam account data
                
            Returns: Processed Steam user account data or empty dict if user not found
        """
        # Check that a user account was return
        json_response = response["response"] if "response" in response else []
        user = json_response.get("players", []) if "players" in json_response else []
        if not user:
            return {}
        
        # get the first and only user that was returned
        user_data = user[0]
        steamid = user_data.get("steamid", "")
        # check the user data is actually our user
        if steamid == "" or steamid != self.user_id:
            return {}
        
        # Extract relevant user account data
        process_data = {
            "steamid": steamid,
            "persona_name": user_data.get("personaname", ""),
            "profile_url": user_data.get("profileurl", ""),
            "avatar_full": user_data.get("avatarfull", ""),
            "real_name": user_data.get("realname", ""),
            "country_code": user_data.get("loccountrycode", ""),
            "state_code": user_data.get("locstatecode", ""),
        }
        
        return process_data
        
    # def _process_wishlist_data(self, response: Dict[str,Any]) -> List[Dict]:
    #     """ 
            
    #     """
    #     items = response["response"].get("items", []) if "response" in response else []
    #     if not items:
    #         return []
        
    #     process_data = []
    #     for item in items:
    #         process_data.append({
    #             "steamid": self.user['steamid'],
    #             "appid": item.get("appid", 0),
    #             "priority": item.get("priority", 9999)
    #         })
            
    #     return process_data
    
    # def _process_library_data(self, response: Dict[str,Any]) -> List[Dict]:
    #     """ 
    #     """
    #     games = response["response"].get("games", []) if "response" in response else []
    #     if not games:
    #         return {}
        
    #     process_data = []
    #     for game in games:
    #         process_data.append({
    #             "steamid": self.user['steamid'],
    #             "appid": game.get("appid", 0),
    #             "priority": game.get("priority", 9999)
    #         })
            
    #     return process_data
    
    # def _process_game_data(self, appid, response: Dict[str,Any]) -> Dict[str,Any]:
    #     """ 
    #     """
    #     is_success = response[appid].get("success", False) if appid in response else False
    #     if not is_success:
    #         return {}
        
    #     data = response[appid].get("data", {}) if appid in response else {}
    #     if not data:
    #         return {}
        
    #     process_data = {
    #         "appid": data.get("steam_appid", 0),
    #         "game_type": data.get("type", ""),
    #         "game_name": data.get("name", ""),
    #         "is_free": data.get("is_free", False),
    #         "detailed_description": data.get("detailed_description", ""),
    #         "about_the_game": data.get("about_the_game", ""),
    #         "header_image": data.get("header_image", ""),
    #         "website": data.get("website", ""),
    #         "developers": data.get("developers", []),
    #         "publishers": data.get("publishers", []),
    #         "categories": data.get("categories", []),
    #         "genres": data.get("genres", [])
    #         # recommendations
    #         # release_date
    #         # rating
    #         # price_overview
    #         # metacritic
    #     }
    #     process_data['recommendations'] = data["recommendations"].get("total", 0) if "recommendations" in data else 0
    #     process_data['release_date'] = data["release_date"].get("date","") if "release_date" in data else ""
        
    #     rating = data["ratings"].get("esrb","rp") if "ratings" in data else "rp"
    #     if rating != "rp":
    #         rating = rating.get("rating", "rp")
    #     process_data["rating"] = rating
        
    #     # steam will sometimes not return certain data if data == 0
    #     price = data["price_overview"] if "price_overview" in data else {}
    #     if not price:
    #         price = {
    #             "currency": "",
    #             "price_in_cents":  0,
    #             "final_formatted": '',
    #             "discount_percentage": 0,
    #         }
    #     else:
    #        price = {
    #             "currency": price.get("currency", ""),
    #             "price_in_cents": price.get("initial", 0), # price is returned in cents
    #             "final_formatted": price.get("final_formatted", ''),
    #             "discount_percentage": price.get("discount_percent", 0),
    #         }  
    #     process_data["price_overview"] = price
        
    #     metacritic = data["metacritic"] if "metacritic" in data else {}
    #     if not metacritic:
    #         metacritic = {
    #             "score": 0,
    #             "url":  ""
    #         }
    #     else:
    #        metacritic = {
    #             "score": metacritic.get("score", 0),
    #             "url": metacritic.get("url", ""),
    #         }  
    #     process_data["metacritic"] = metacritic
        
    #     return process_data