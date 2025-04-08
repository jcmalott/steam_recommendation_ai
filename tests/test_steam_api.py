import pytest
from unittest.mock import patch, Mock
import json
import requests

from src.steam_api import Steam
import test_data

@pytest.fixture
def steam_api():
    """Create a Steam API instance with test credentials."""
    return Steam(steam_api_key=test_data.STEAM_API_KEY, user_id=test_data.STEAM_USER_ID)

def test_init_calls_check_user_account(steam_api: Steam):
    """Test that the constructor sets api key and user_id"""
    assert steam_api.steam_api_key == test_data.STEAM_API_KEY
    assert steam_api.user_id == test_data.STEAM_USER_ID

@pytest.mark.parametrize("actual, expected", [
    (test_data.SAMPLE_USER_RESPONSE, test_data.GET_STEAM_USER_SUCCESS),
    (test_data.SAMPLE_EMPTY_USER_RESPONSE, {}),
    (test_data.SAMPLE_ONLY_STEAMID_RESPONSE, test_data.GET_STEAM_USER_ID_ONLY),
    (test_data.GET_STEAM_USER_INVALID_ID, {})
])
def test_check_user_account(actual, expected, steam_api: Steam):
    """Test that check_user_account properly processes a successful response."""
    with patch('requests.get') as mock_get:
        # Configure the mock to return a successful response
        mock_response = Mock()
        mock_response.json.return_value = actual
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        user_data = steam_api.check_user_account()
        
        assert user_data == expected
        _check_params(test_data.STEAM_USER_URL, mock_get)

# def test_check_user_account_request_exception():
#     """Test that check_user_account handles request exceptions."""
#     with patch('requests.get') as mock_get:
#         # Configure the mock to raise an exception
#         mock_get.side_effect = requests.RequestException("API Error")
        
#         with pytest.raises(ValueError) as excinfo:
#             steam = Steam(steam_api_key="test_api_key", user_id="76561198041511379")
        
#         #  Verify the exception has the expected message including the specific user ID
#         assert str(excinfo.value) == "Failed to retrieve UserId 76561198041511379!"
        
#         _check_params(mock_get)

# @pytest.mark.parametrize("actual, expected", [
#     (test_data.SAMPLE_USER_RESPONSE, test_data.GET_STEAM_USER_SUCCESS),
#     (test_data.SAMPLE_PARTIAL_RESPONSE, test_data.GET_STEAM_USER_ID_ONLY),
#     (test_data.SAMPLE_EMPTY_USER_RESPONSE, {}),
#     ({"invalid": "structure"}, {}),
#     ({"response": "structure"}, {})
# ])
# def test_process_user_data(actual, expected):
#     with patch.object(Steam, 'check_user_account') as mock_get_data:
#         mock_get_data.return_value = {"steamid": "76561198041511379"}
#         steam = Steam(steam_api_key="test_api_key", user_id="76561198041511379")
        
#         # Test with a complete response
#         result = steam._process_user_data(actual)
#         assert result == expected
        
# def test_get_wishlist():
#     with patch('requests.get') as mock_get:
#         mock_response = Mock()
#         mock_response.json.return_value = test_data.SAMPLE_WISHLIST_RESPONSE
#         mock_response.raise_for_status.return_vale = None
#         mock_get.return_value  = mock_response
        
#         steam_api = Steam(steam_api_key="test_api_key", user_id="76561198041511379")
#         _check_params(mock_get)
        
#         wishlist_items = steam_api.get_wishlist()
#         assert wishlist_items == test_data.GET_STEAM_WISHLIST
        
def _check_params(url: str, mock_get: Mock):
    # Verify that requests.get was called once before the exception was raised
    # Verify the correct URL and parameters were used in the API call
    mock_get.assert_called_once_with(
        url,
        params={'key': test_data.STEAM_API_KEY, 'steamids': test_data.STEAM_USER_ID}
    )