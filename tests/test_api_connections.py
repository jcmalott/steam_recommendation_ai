import os
from dotenv import load_dotenv
import pytest
import json
import requests

import test_data
from src import logger
from data.steam_database import SteamDatabase

load_dotenv()
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
STEAM_USER_ID = os.getenv('STEAM_USER_ID')

@pytest.mark.parametrize("url, params, json_keys",[
        (test_data.STEAM_USER_URL, {'key': STEAM_API_KEY, 'steamids': test_data.STEAM_USER_ID}, ['response','players']),
        (test_data.STEAM_WISHLIST_URL, {'key': STEAM_API_KEY, 'steamid': test_data.STEAM_USER_ID}, ['response','items']),
        (test_data.STEAM_GAME_URL, {'appids': 21130}, ['21130','data']),
        (test_data.STEAM_LIBRARY_URL, {'key': STEAM_API_KEY, 'steamid': test_data.STEAM_USER_ID}, ['response','games'])
    ])
def test_steam_api_connection(url, params, json_keys):
    response = _api_connection_test(url, params, json_keys)
    assert response['connected'] == True
    assert response['correct_keys'] == True
    
def _api_connection_test(api_url, params, keys, timeout=10):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        correct_keys = False
        json_response = response.json()
        if keys[0] in json_response and keys[1] in json_response[keys[0]]:
            correct_keys = True
        
        return {'connected': True, 'correct_keys': correct_keys}
    except requests.RequestException as e:
        logger.error(f"API connection failed: {e}")
        return {'connected': False, 'correct_keys': False}
    
def test_database_connection():
    db = SteamDatabase('steam', 'postgres', DATABASE_PASSWORD)
    is_connected = db._check_table_item('steamid','users', STEAM_USER_ID)
    assert is_connected == True