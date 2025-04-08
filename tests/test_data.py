STEAM_WISHLIST_URL = 'https://api.steampowered.com/IWishlistService/GetWishlist/v1'
STEAM_LIBRARY_URL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
STEAM_GAME_URL = 'https://store.steampowered.com/api/appdetails'
STEAM_USER_URL = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
STEAM_API_KEY="test_api_key"
STEAM_USER_ID="76561198041511379"

# Sample test data for mocking responses
SAMPLE_USER_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": "76561198041511379",
                "personaname": "Test User",
                "profileurl": "https://steamcommunity.com/id/testuser/",
                "avatarfull": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/test.jpg",
                "realname": "Real Test Name",
                "loccountrycode": "US",
                "locstatecode": "CA"
            }
        ]
    }
}
SAMPLE_ONLY_STEAMID_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": "76561198041511379",
                "personaname": "",
                "profileurl": "",
                "avatarfull": "",
                "realname": "",
                "loccountrycode": "",
                "locstatecode": ""
            }
        ]
    }
}
SAMPLE_EMPTY_USER_RESPONSE = {
    "response": {
        "players": []
    }
}
GET_STEAM_USER_INVALID_ID = {
    "response": {
        "players": [
            {
                "steamid": "different_id",
                "personaname": "Test User",
                "profileurl": "https://steamcommunity.com/id/testuser/",
                "avatarfull": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/test.jpg",
                "realname": "Real Test Name",
                "loccountrycode": "US",
                "locstatecode": "CA"
            }
        ]
    }
}
SAMPLE_PARTIAL_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": "76561198041511379",
                # Missing other fields
            }
        ]
    }
}
SAMPLE_WISHLIST_RESPONSE = {
    "response": {
        "items": [
            {
                "appid": 16900,
                "priority": 303,
                "date_added": 1689263421
            }
        ]
    }
}


# PROCESS DATA
GET_STEAM_USER_SUCCESS = {
    "steamid": "76561198041511379",
    "persona_name": "Test User",
    "profile_url": "https://steamcommunity.com/id/testuser/",
    "avatar_full": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/test.jpg",
    "real_name": "Real Test Name",
    "country_code": "US",
    "state_code": "CA"
}
GET_STEAM_USER_ID_ONLY = {
    "steamid": "76561198041511379",
    "persona_name": "",
    "profile_url": "",
    "avatar_full": "",
    "real_name": "",
    "country_code": "",
    "state_code": ""         
}
GET_STEAM_WISHLIST = [{
    "steamid": "76561198041511379",
    "appid": 16900,
    "priority": 303
}]