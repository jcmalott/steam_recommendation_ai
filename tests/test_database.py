import pytest
import psycopg2 as pg2
from unittest.mock import patch, Mock, MagicMock

from data.steam_database import SteamDatabase
import test_data


@pytest.fixture
def mock_conn():
    """Create a mock connection for database operations."""
    conn = MagicMock()
    conn.cursor.return_value = MagicMock()
    return conn

@pytest.fixture
def db(mock_conn):
    """Create a SteamDatabase instance with a mocked connection."""
    with patch('psycopg2.connect', return_value=mock_conn):
        db = SteamDatabase(database="test_db", user="test_user", password="test_password")
        db.conn = mock_conn
        db.cur = mock_conn.cursor()
        return db

def test_init_connects_to_database():
    """Test that the constructor establishes a database connection."""
    with patch('psycopg2.connect') as mock_connect:
        db = SteamDatabase(database="test_db", user="test_user", password="test_password")
        
        assert db.conn == mock_connect.return_value
        assert db.cur == mock_connect.return_value.cursor.return_value
        
        # check if connection was called
        mock_connect.assert_called_once_with(
            database="test_db", 
            user="test_user", 
            password="test_password"
        )

def test_add_steam_user_new_user(db: SteamDatabase):
    """Test adding a new user to the database."""
    # Mock _check_table_item to return False (user doesn't exist)
    with patch.object(db, '_check_table_item', return_value=False):
        # Mock _insert_new_row
        with patch.object(db, '_insert_new_row') as mock_insert:
            result = db.add_steam_user(test_data.GET_STEAM_USER_SUCCESS)
            assert result == True
            
            # Verify _check_table_item was called with the correct parameters
            db._check_table_item.assert_called_once_with('steamid', 'users', test_data.GET_STEAM_USER_SUCCESS['steamid'])
    
            # Verify _insert_new_row was called with the correct parameters
            expected_fields = ['steamid', 'persona_name', 'profile_url', 'avatar_full', 'real_name', 'country_code', 'state_code']
            mock_insert.assert_called_once_with('users', expected_fields, test_data.GET_STEAM_USER_SUCCESS)

def test_add_steam_user_existing_user(db: SteamDatabase):
    """Test adding a user that already exists in the database."""
    # Mock _check_table_item to return True (user exists)
    with patch.object(db, '_check_table_item', return_value=True):
        # Mock _insert_new_row
        with patch.object(db, '_insert_new_row') as mock_insert:
            result = db.add_steam_user(test_data.GET_STEAM_USER_SUCCESS)
            # Verify the result is False (user already existed)
            assert result == False
            
            # Verify _check_table_item was called with the correct parameters
            db._check_table_item.assert_called_once_with('steamid', 'users', test_data.GET_STEAM_USER_SUCCESS['steamid'])
            # Verify _insert_new_row was not called
            mock_insert.assert_not_called()

def test_check_update_status_user_not_found(db: SteamDatabase):
    """Test check_update_status when the user is not found in the database."""
    # Mock _check_table_item to return False (user doesn't exist)
    with patch.object(db, '_check_table_item', return_value=False):
        result = db.check_update_status("765611980415113", "wishlist_update_at")
        # Verify the result is False (data needs to be updated)
        assert result == False
        
        # Verify _check_table_item was called with the correct parameters
        db._check_table_item.assert_called_once_with('steamid', 'schedule_data_retrieval', "765611980415113")
        # Verify execute was not called
        db.cur.execute.assert_not_called()

def test_check_update_status_success(db: SteamDatabase):
    """Test check_update_status when the user is found and query is successful."""
    # Mock _check_table_item to return True (user exists)
    with patch.object(db, '_check_table_item', return_value=True):
        # Mock cursor.fetchone to return True (update needed)
        db.cur.fetchone.return_value = True
        test_steamid = test_data.GET_STEAM_USER_SUCCESS['steamid']
        result = db.check_update_status(test_steamid, "wishlist_update_at")
        
        # Verify the result is True (update needed)
        assert result == True
        
        # Verify _check_table_item was called with the correct parameters
        db._check_table_item.assert_called_once_with('steamid', 'schedule_data_retrieval', test_steamid)
        
        # Verify execute was called with the correct query
        expected_query = f"""
                SELECT needs_retrieval(wishlist_update_at) 
                FROM schedule_data_retrieval 
                WHERE steamid = '{test_steamid}';
            """
        db.cur.execute.assert_called_once_with(expected_query)

def test_check_update_status_database_error(db: SteamDatabase):
    """Test check_update_status when a database error occurs."""
    # Mock _check_table_item to return True (user exists)
    with patch.object(db, '_check_table_item', return_value=True):
        # Mock cursor.execute to raise a database error
        db.cur.execute.side_effect = pg2.Error("Database error")
        
        result = db.check_update_status("76561198041511379", "wishlist_update_at")
        # Verify the result is None (error occurred)
        assert result is None
        
        # Verify _check_table_item was called with the correct parameters
        db._check_table_item.assert_called_once_with('steamid', 'schedule_data_retrieval', "76561198041511379")
        # Verify rollback was called
        db.conn.rollback.assert_called_once()

def test_insert_new_row_success(db: SteamDatabase):
    """Test _insert_new_row with a successful insertion."""
    fields = ['field1', 'field2']
    items = {'field1': 'value1', 'field2': 'value2'}
    
    db._insert_new_row('test_table', fields, items)
    
    # Verify execute was called with the correct query and parameters
    expected_query = """
                INSERT INTO test_table (field1, field2)
                VALUES (%s, %s)
            """
    db.cur.execute.assert_called_once_with(expected_query, ['value1', 'value2'])
    # Verify commit was called
    db.conn.commit.assert_called_once()

def test_insert_new_row_database_error(db: SteamDatabase):
    """Test _insert_new_row when a database error occurs."""
    fields = ['field1', 'field2']
    items = {'field1': 'value1', 'field2': 'value2'}
    
    # Mock cursor.execute to raise a database error
    db.cur.execute.side_effect = pg2.Error("Database error")
    
    db._insert_new_row('test_table', fields, items)
    # Verify rollback was called
    db.conn.rollback.assert_called_once()

@pytest.mark.parametrize("return_value, expected", [
    #Test _check_table_item when the item is found.
    ('76561198041511379', True),
    #Test _check_table_item when the item is not found.
    (None, False)
])
def test_check_table_item_found(return_value, expected, db: SteamDatabase):
    # Mock cursor.fetchone to return a value (item found)
    db.cur.fetchone.return_value = (return_value)
    result = db._check_table_item('steamid', 'users', '76561198041511379')
    assert result == expected
    
    # Verify execute was called with the correct query
    expected_query = "SELECT steamid FROM users WHERE steamid = '76561198041511379'"
    db.cur.execute.assert_called_once_with(expected_query)

def test_check_table_item_database_error(db: SteamDatabase):
    """Test _check_table_item when a database error occurs."""
    # Mock cursor.execute to raise a database error
    db.cur.execute.side_effect = pg2.Error("Database error")
    
    result = db._check_table_item('steamid', 'users', '76561198041511379')
    # Verify the result is False (error occurred)
    assert result == False