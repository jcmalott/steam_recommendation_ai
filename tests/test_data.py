STEAM_WISHLIST_URL = 'https://api.steampowered.com/IWishlistService/GetWishlist/v1'
STEAM_LIBRARY_URL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
STEAM_GAME_URL = 'https://store.steampowered.com/api/appdetails'
STEAM_USER_URL = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
STEAM_API_KEY="test_api_key"
STEAM_USER_ID="76561198041511379"

DATABASE_USER="test_user"
DATABASE_NAME="test_db"
DATABASE_PASSWORD="test_password"

# ------------------------
# -----  CHECK USER  -----
# ------------------------
CORRECT_USER_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": STEAM_USER_ID,
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
ONLY_STEAMID_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": STEAM_USER_ID,
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
EMPTY_USER_RESPONSE = {
    "response": {
        "players": []
    }
}
INVALID_USER_ID_RESPONSE = {
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
PARTIAL_USER_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": STEAM_USER_ID,
                # Missing other fields
            }
        ]
    }
}

# PROCESS DATA
CORRECT_USER_PROCESSED = {
    "steamid": STEAM_USER_ID,
    "persona_name": "Test User",
    "profile_url": "https://steamcommunity.com/id/testuser/",
    "avatar_full": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/test.jpg",
    "real_name": "Real Test Name",
    "country_code": "US",
    "state_code": "CA"
}
USER_ID_ONLY_PROCESSED = {
    "steamid": STEAM_USER_ID,
    "persona_name": "",
    "profile_url": "",
    "avatar_full": "",
    "real_name": "",
    "country_code": "",
    "state_code": ""         
}


# ------------------------
# ------  WISHLIST  ------
# ------------------------
CORRECT_WISHLIST_RESPONSE = {
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
PARTIAL_WISHLIST_RESPONSE = {
    "response": {
        "items": [
            {
                "appid": 16900,
            }
        ]
    }
}
EMPTY_WISHLIST_RESPONSE = {
    "response": {
        "items": [{}]
    }
}
DB_WISHLIST_RESPONSE = [
    ('76561198041511379',  362490, 253),
    ('76561198041511379',  362680, 132) 
]


# PROCESS DATA
CORRECT_WISHLIST_PROCESSED = [{
    "steamid": STEAM_USER_ID,
    "appid": 16900,
    "priority": 303
}]
WISHLIST = [
    {
        'steamid': STEAM_USER_ID,
        "appid": 16900,
        "priority": 303
    },
    {
        'steamid': STEAM_USER_ID,
        "appid": 34010,
        "priority": 424
    }
]
DB_WISHLIST_PROCESSED = [
    {'steamid': '76561198041511379', 'appid': 362490, 'priority': 253}, 
    {'steamid': '76561198041511379', 'appid': 362680, 'priority': 132}
]


# ------------------------
# ------  LIBRARY  -------
# ------------------------
CORRECT_LIBRARY_RESPONSE = {
    "response": {
        "game_count": 469,
        "games": [
            {
                "appid": 4000,
                "playtime_forever": 282,
                "playtime_windows_forever": 0,
                "playtime_mac_forever": 0,
                "playtime_linux_forever": 0,
                "playtime_deck_forever": 0,
                "rtime_last_played": 1547887933,
                "playtime_disconnected": 0
            }
        ]
    }
}
EMPTY_LIBRARY_RESPONSE = {
    "response": {
        "games": [{}]
    }
}
DB_LIBRARY_RESPONSE = [
    ('76561198041511379',  362490, 253),
    ('76561198041511379',  362680, 132) 
]

# PROCESS DATA
CORRECT_LIBRARY_PROCESSED = [
    {
        'steamid': STEAM_USER_ID,
        "appid": 4000,
        "playtime_minutes": 282
    }
]
DB_LIBRARY_PROCESSED = [
    {'steamid': STEAM_USER_ID, 'appid': 362490, 'playtime_minutes': 253},
    {'steamid': STEAM_USER_ID, 'appid': 362680, 'playtime_minutes': 132}
]