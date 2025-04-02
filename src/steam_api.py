""" 
    https://api.steampowered.com/IWishlistService/GetWishlist/v1?steamid=76561198041511379
    Wishlist
    
    https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=09A19535C0064A3301527FD3AE352D7E&steamid=76561198041511379&format=json&include_played_free_games=True
    In Library
    
    https://store.steampowered.com/api/appdetails?appids=532790
    Game Info
    
    https://www.kinguin.net/app/dashboard/orders 
    https://store.steampowered.com/account/history/ 
    * You will need to click within each item to see its cost and discount
    *   - if a list of items was bought, you need to click the list above for each items cost and discount
    Purchase History
    * Could be a good idea to add games you have from different librays
"""
import requests
from typing import Dict, Any, List
import logging

""" 
    STEAM CLASS
    * Every method when done should store data to database
    - get_wishlist
        Only need to call once
            ["response"]["items"] = [{}]
            - appid
    - get_libray
        Only need to call once
            ["response"]["games"] = [{}]
            - appid
            - playtime_forever
    - get_game_data
        # wait 1.5 secs between each call, 200 request per 5 mins = (5*60)/200 = 1.5
        Need to call for every game 
            # appid -> Enter the acctual app id EX: ["1091500"]["success"] = True
            [appid]["success"] = bool #if item was found
            [appid]["data"] = {}
            - name, steam_appid, is_free, detailed_description, about_the_game, header_image, website, developers, publishers
            * price is given in cents
            - price_overview -> currency, initial, final, discount_percent
            - metacritic - > score
            - categories - > description
            - genres - > description
            - recommendations - > total
            * Dec 9, 2020
            - release_date - > date
            - ratings - > esrb
"""
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Steam():
    """ 
    """
    STEAM_WISHLIST_URL = 'https://api.steampowered.com/IWishlistService/GetWishlist/v1'
    STEAM_LIBRARY_URL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    STEAM_GAME_URL = 'https://store.steampowered.com/api/appdetails'
    STEAM_USER_URL = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    
    def __init__(self, steam_api_key: str, user_id: str):
        """ 
        """
        self.steam_api_key = steam_api_key
        self.user = self._get_steam_user_data(steam_api_key, user_id)
        
    def get_wishlist(self) -> List[str]:
        """ 
            * When updating a wishlist you will need to delete and add wishlist items stored in database
        """
        user_id = self.user['steamid']
        params = {
            'key': self.steam_api_key,
            'steamid': user_id
        }
        
        try:
            response = requests.get(self.STEAM_WISHLIST_URL, params=params)
            response.raise_for_status()
            
            data = self._process_wishlist_data(response.json())
            # save data to database
            # only download this data once a day
            # TODO do use db here
            # db.add_to_wishlist(user_id, data)
            if not data:
                logger.warning(f"UserId: {user_id} has no wishlist items!")
                
            return data
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve wishlist from UserId {user_id}!")
        
    def get_library(self):
        """ 
        """
        params = {
            'key': self.steam_api_key,
            'steamid': self.user['steamid'],
            'format': 'json',
            'include_played_free_games': True
        }
        
        data = self._process_library_data()
        
    def get_game_data(self, appid):
        """ 
        """
        params = {
            'appids': appid
        }
        
        self._process_game_data(appid)
        
    def get_user_data(self):
        return self.user
        
    def _get_steam_user_data(self, steam_api_key, user_id) -> Dict[str, Any]:
        params = {
            'key': steam_api_key,
            'steamids': user_id
        }
        
        try:
            logger.info(f"Steam User URL: {self.STEAM_USER_URL}?key={params['key']}&steamids={params['steamids']}")
            response = requests.get(self.STEAM_USER_URL, params=params)
            response.raise_for_status()
            
            data = self._process_user_data(response.json())
            if not data:
                logger.warning(f"Steam UserId: {user_id} doesn't exist!")
                # TODO throw exception for user not found
            
            return data
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve UserId {user_id}!")
            # TODO catch user not found exception
            
    def _process_user_data(self, response: Dict[str,Any]) -> Dict[str, Any]:
        """ 
            * Createa a custom exception for no user id
        """
        user = response["response"].get("players", []) if "response" in response else []
        if not user:
            return {}
        
        user_data = user[0]
        steamid = user_data.get("steamid", "")
        if steamid == "":
            return {}
        
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
        
    def _process_wishlist_data(self, response: Dict[str,Any]) -> List[Dict]:
        """ 
            
        """
        items = response["response"].get("items", []) if "response" in response else []
        if not items:
            return []
        
        process_data = []
        for item in items:
            process_data.append({
                "appid": item.get("appid", 0),
                "priority": item.get("priority", 9999)
            })
            
        return process_data
    
    def _process_library_data(self, response: Dict[str,Any]) -> List[Dict]:
        """ 
        """
        games = response["response"].get("games", []) if "response" in response else []
        if not games:
            return {}
        
        process_data = []
        for game in games:
            process_data.append({
                "steamid": self.user['steamid'],
                "appid": game.get("appid", 0),
                "priority": game.get("priority", 9999)
            })
            
        return process_data
    
    def _process_game_data(self, appid, response: Dict[str,Any]) -> Dict[str,Any]:
        """ 
        """
        is_success = response[appid].get("success", False) if appid in response else False
        if not is_success:
            return {}
        
        data = response[appid].get("data", {}) if appid in response else {}
        if not data:
            return {}
        
        process_data = {
            "appid": data.get("steam_appid", 0),
            "game_type": data.get("type", ""),
            "game_name": data.get("name", ""),
            "is_free": data.get("is_free", False),
            "detailed_description": data.get("detailed_description", ""),
            "about_the_game": data.get("about_the_game", ""),
            "header_image": data.get("header_image", ""),
            "website": data.get("website", ""),
            "developers": data.get("developers", []),
            "publishers": data.get("publishers", []),
            "categories": data.get("categories", []),
            "genres": data.get("genres", [])
            # recommendations
            # release_date
            # rating
            # price_overview
            # metacritic
        }
        process_data['recommendations'] = data["recommendations"].get("total", 0) if "recommendations" in data else 0
        process_data['release_date'] = data["release_date"].get("date","") if "release_date" in data else ""
        
        rating = data["ratings"].get("esrb","rp") if "ratings" in data else "rp"
        if rating != "rp":
            rating = rating.get("rating", "rp")
        process_data["rating"] = rating
        
        # steam will sometimes not return certain data if data == 0
        price = data["price_overview"] if "price_overview" in data else {}
        if not price:
            price = {
                "currency": "",
                "price_in_cents":  0,
                "final_formatted": '',
                "discount_percentage": 0,
            }
        else:
           price = {
                "currency": price.get("currency", ""),
                "price_in_cents": price.get("initial", 0), # price is returned in cents
                "final_formatted": price.get("final_formatted", ''),
                "discount_percentage": price.get("discount_percent", 0),
            }  
        process_data["price_overview"] = price
        
        metacritic = data["metacritic"] if "metacritic" in data else {}
        if not metacritic:
            metacritic = {
                "score": 0,
                "url":  ""
            }
        else:
           metacritic = {
                "score": metacritic.get("score", 0),
                "url": metacritic.get("url", ""),
            }  
        process_data["metacritic"] = metacritic
        
        return process_data