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