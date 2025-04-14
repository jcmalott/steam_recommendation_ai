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

# ------------------------
# -------  USER  ---------
# ------------------------
def test_init_calls_check_user_account(steam_api: Steam):
    """Test that the constructor sets api key and user_id"""
    assert steam_api.steam_api_key == test_data.STEAM_API_KEY
    assert steam_api.user_id == test_data.STEAM_USER_ID

@pytest.mark.parametrize("actual, expected", [
    (test_data.CORRECT_USER_RESPONSE, test_data.CORRECT_USER_PROCESSED),
    (test_data.EMPTY_USER_RESPONSE, {}),
    (test_data.ONLY_STEAMID_RESPONSE , test_data.USER_ID_ONLY_PROCESSED),
    (test_data.INVALID_USER_ID_RESPONSE, {})
])
def test_check_user_account(actual, expected, steam_api: Steam):
    """Test that check_user_account properly process"""
    with patch('requests.get') as mock_get:
        # Configure the mock to return a successful response
        mock_response = Mock()
        mock_response.json.return_value = actual
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        user_data = steam_api.check_user_account()
        
        assert user_data == expected
        mock_get.assert_called_once_with(
            test_data.STEAM_USER_URL,
            params={'key': test_data.STEAM_API_KEY, 'steamids': test_data.STEAM_USER_ID}
        )

def test_check_user_account_request_exception(steam_api: Steam):
    """Test that check_user_account handles request exceptions."""
    with patch('requests.get') as mock_get:
        # Configure the mock to raise an exception
        mock_get.side_effect = requests.RequestException("API Error")
        
        with pytest.raises(ValueError) as excinfo:
            steam_api.check_user_account()
        
        #  Verify the exception has the expected message including the specific user ID
        assert str(excinfo.value) == f"Failed to retrieve UserId {test_data.STEAM_USER_ID}!"
        
        mock_get.assert_called_once_with(
            test_data.STEAM_USER_URL,
            params={'key': test_data.STEAM_API_KEY, 'steamids': test_data.STEAM_USER_ID}
        )

@pytest.mark.parametrize("actual, expected", [
    (test_data.CORRECT_USER_RESPONSE, test_data.CORRECT_USER_PROCESSED),
    (test_data.PARTIAL_USER_RESPONSE, test_data.USER_ID_ONLY_PROCESSED),
    (test_data.INVALID_USER_ID_RESPONSE, {}),
    # Test invalid response key
    ({"invalid": "structure"}, {}),
    # Test invalid response players key
    ({"response": "structure"}, {})
])
def test_process_user_data(actual, expected, steam_api: Steam):
    # Test with a complete response
    result = steam_api._process_user_data(actual)
    assert result == expected


# ------------------------
# ------  WISHLIST  ------
# ------------------------
def test_get_wishlist(steam_api: Steam):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = test_data.CORRECT_WISHLIST_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value  = mock_response
        
        wishlist_items = steam_api.get_wishlist()
        assert wishlist_items == test_data.CORRECT_WISHLIST_PROCESSED
        
        mock_get.assert_called_once_with(
        test_data.STEAM_WISHLIST_URL,
        params={'key': test_data.STEAM_API_KEY, 'steamid': test_data.STEAM_USER_ID}
    )
        
def test_get_wishlist_request_exception(steam_api: Steam):
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.RequestException("API Error")
        
        with pytest.raises(requests.RequestException) as excinfo:
            steam_api.get_wishlist()
        assert str(excinfo.value) == f"Failed to retrieve wishlist for UserId {test_data.STEAM_USER_ID}!"
        
        mock_get.assert_called_once_with(
        test_data.STEAM_WISHLIST_URL,
        params={'key': test_data.STEAM_API_KEY, 'steamid': test_data.STEAM_USER_ID}
    )

@pytest.mark.parametrize("actual, expected", [
    (test_data.CORRECT_WISHLIST_RESPONSE, test_data.CORRECT_WISHLIST_PROCESSED),
    (test_data.EMPTY_WISHLIST_RESPONSE, []),
    # Test invalid response key
    ({"invalid": "structure"}, []),
    # Test invalid response items key
    ({"response": "structure"}, [])
])        
def test_process_wishlist_data(actual, expected, steam_api: Steam):
    wishlist = steam_api._process_wishlist_data(actual)
    assert wishlist == expected

# ------------------------
# ------  LIBRARY  -------
# ------------------------    
def test_get_library(steam_api: Steam):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = test_data.CORRECT_LIBRARY_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value  = mock_response
        
        library_items = steam_api.get_library()
        assert library_items == test_data.CORRECT_LIBRARY_PROCESSED
        
        mock_get.assert_called_once_with(
            test_data.STEAM_LIBRARY_URL,
            params={
                'key': test_data.STEAM_API_KEY,
                'steamid': test_data.STEAM_USER_ID,
                'format': 'json',
                'include_played_free_games': True
            }
        )
        
def test_get_library_request_exception(steam_api: Steam):
    """Test that check_user_account handles request exceptions."""
    with patch('requests.get') as mock_get:
        # Configure the mock to raise an exception
        mock_get.side_effect = requests.RequestException("API Error")
        
        with pytest.raises(requests.RequestException) as excinfo:
            steam_api.get_library()
        
        #  Verify the exception has the expected message including the specific user ID
        assert str(excinfo.value) == f"Failed to retrieve library for UserId {test_data.STEAM_USER_ID}!"
        
        mock_get.assert_called_once_with(
            test_data.STEAM_LIBRARY_URL,
            params={
                'key': test_data.STEAM_API_KEY,
                'steamid': test_data.STEAM_USER_ID,
                'format': 'json',
                'include_played_free_games': True
            }
        )

@pytest.mark.parametrize("actual, expected", [
    (test_data.CORRECT_LIBRARY_RESPONSE, test_data.CORRECT_LIBRARY_PROCESSED),
    (test_data.EMPTY_LIBRARY_RESPONSE, []),
    # Test invalid response key
    ({"invalid": "structure"}, []),
    # Test invalid response items key
    ({"response": "structure"}, [])
])     
def test_process_library_data(actual, expected, steam_api: Steam):
    library = steam_api._process_library_data(actual)
    assert library == expected