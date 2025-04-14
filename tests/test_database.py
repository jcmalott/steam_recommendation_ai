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
        db = SteamDatabase(database=test_data.DATABASE_NAME, user=test_data.DATABASE_USER, password=test_data.DATABASE_PASSWORD)
        db.conn = mock_conn
        db.cur = mock_conn.cursor()
        return db

def test_init_connects_to_database():
    """Test that the constructor establishes a database connection."""
    with patch('psycopg2.connect') as mock_connect:
        db = SteamDatabase(database=test_data.DATABASE_NAME, user=test_data.DATABASE_USER, password=test_data.DATABASE_PASSWORD)
        
        assert db.conn == mock_connect.return_value
        assert db.cur == mock_connect.return_value.cursor.return_value
        
        # check if connection was called
        mock_connect.assert_called_once_with(
            database="test_db", 
            user="test_user", 
            password="test_password"
        )
        
@pytest.mark.parametrize("return_value, expected", [
    #Test _check_table_item when the item is found.
    (test_data.STEAM_USER_ID, True),
    #Test _check_table_item when the item is not found.
    (None, False)
])
def test_check_table_item_found(return_value, expected, db: SteamDatabase):
    # Mock cursor.fetchone to return a value (item found)
    db.cur.fetchone.return_value = (return_value)
    result = db._check_table_item('steamid', 'users', test_data.STEAM_USER_ID)
    assert result == expected
    
    # Verify execute was called with the correct query
    expected_query = f"SELECT steamid FROM users WHERE steamid = '{test_data.STEAM_USER_ID}'"
    db.cur.execute.assert_called_once_with(expected_query)

def test_check_table_item_database_error(db: SteamDatabase):
    """Test _check_table_item when a database error occurs."""
    # Mock cursor.execute to raise a database error
    db.cur.execute.side_effect = pg2.Error("Database error")
    
    result = db._check_table_item('steamid', 'users', '76561198041511379')
    # Verify the result is False (error occurred)
    assert result == False   
    
def test_insert_new_row_success(db: SteamDatabase):
    """Test _insert_new_row with a successful insertion."""
    fields = ['field1', 'field2']
    items = {'field1': 'value1', 'field2': 'value2'}
    
    result = db._insert_new_row('test_table', fields, [items])
    
    assert result == True
    # Verify execute was called with the correct query and parameters
    expected_query = """
                INSERT INTO test_table (field1, field2)
                VALUES (%s, %s)
            """
    db.cur.executemany.assert_called_once_with(expected_query, [['value1', 'value2']])
    # Verify commit was called
    db.conn.commit.assert_called_once()

def test_insert_new_row_database_error(db: SteamDatabase):
    """Test _insert_new_row when a database error occurs."""
    fields = ['field1', 'field2']
    items = {'field1': 'value1', 'field2': 'value2'}
    
    # Mock cursor.execute to raise a database error
    db.cur.executemany.side_effect = pg2.Error("Database error")
    
    result = db._insert_new_row('test_table', fields, [items])
    assert not result
    
    # Verify rollback was called
    db.conn.rollback.assert_called_once()
    

def test_add_steam_user_new_user(db: SteamDatabase):
    """Test adding a new user to the database."""
    # Mock _check_table_item to return False (user doesn't exist)
    with patch.object(db, '_check_table_item', return_value=False):
        # Mock _insert_new_row
        with patch.object(db, '_insert_new_row') as mock_insert:
            result = db.add_steam_user(test_data.CORRECT_USER_PROCESSED)
            assert result == True
            
            # Verify _check_table_item was called with the correct parameters
            db._check_table_item.assert_called_once_with('steamid', 'users', test_data.CORRECT_USER_PROCESSED['steamid'])
    
            # Verify _insert_new_row was called with the correct parameters
            expected_fields = ['steamid', 'persona_name', 'profile_url', 'avatar_full', 'real_name', 'country_code', 'state_code']
            mock_insert.assert_called_once_with('users', expected_fields, [test_data.CORRECT_USER_PROCESSED])

def test_add_steam_user_existing_user(db: SteamDatabase):
    """Test adding a user that already exists in the database."""
    # Mock _check_table_item to return True (user exists)
    with patch.object(db, '_check_table_item', return_value=True):
        # Mock _insert_new_row
        with patch.object(db, '_insert_new_row') as mock_insert:
            result = db.add_steam_user(test_data.CORRECT_USER_PROCESSED)
            # Verify the result is False (user already existed)
            assert result == False
            
            # Verify _check_table_item was called with the correct parameters
            db._check_table_item.assert_called_once_with('steamid', 'users', test_data.CORRECT_USER_PROCESSED['steamid'])
            # Verify _insert_new_row was not called
            mock_insert.assert_not_called()

def test_check_update_status_user_not_found(db: SteamDatabase):
    """Test check_update_status when the user is not found in the database."""
    # Mock _check_table_item to return False (user doesn't exist)
    with patch.object(db, '_check_table_item', return_value=False):
        result = db.check_update_status("765611980415113", "wishlist_update_at")
        # Verify the result is False (data needs to be updated)
        assert result == True
        
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
        result = db.check_update_status(test_data.STEAM_USER_ID, "wishlist_updated_at")
        
        # Verify the result is True (update needed)
        assert result == True
        
        # Verify _check_table_item was called with the correct parameters
        db._check_table_item.assert_called_once_with('steamid', 'schedule_data_retrieval', test_data.STEAM_USER_ID)
        
        # Verify execute was called with the correct query
        expected_query = f"""
                SELECT needs_retrieval(wishlist_updated_at) 
                FROM schedule_data_retrieval 
                WHERE steamid = '{test_data.STEAM_USER_ID}';
            """
            
        # query being called within the method
        actual_query = db.cur.execute.call_args[0][0]
        assert normalize_sql(actual_query) == normalize_sql(expected_query)

def test_check_update_status_database_error(db: SteamDatabase):
    """Test check_update_status when a database error occurs."""
    # Mock _check_table_item to return True (user exists)
    with patch.object(db, '_check_table_item', return_value=True):
        # Mock cursor.execute to raise a database error
        db.cur.execute.side_effect = pg2.Error("Database error")
        
        result = db.check_update_status(test_data.STEAM_USER_ID, "wishlist_update_at")
        # Verify the result is None (error occurred)
        assert result == True
        
        # Verify _check_table_item was called with the correct parameters
        db._check_table_item.assert_called_once_with('steamid', 'schedule_data_retrieval', test_data.STEAM_USER_ID)
        # Verify rollback was called
        db.conn.rollback.assert_called_once()
        
def test_add_wishlist(db: SteamDatabase):
    with patch.object(db, '_check_table_item', return_value=True):
        # mock insert row
        with patch.object(db, '_insert_new_row') as mock_insert:
            items = db.add_to_wishlist(test_data.STEAM_USER_ID, test_data.WISHLIST)
            assert items > 0
            
            # Verify _check_table_item was called with the correct parameters
            db._check_table_item.assert_called_once_with('steamid', 'users', test_data.STEAM_USER_ID)
            
            # check correct query was created
            expected_query = f"""
                ON CONFLICT (steamid, appid)
                DO UPDATE SET
                priority = EXCLUDED.priority
            """
            actual_query = mock_insert.call_args[0][3]
            assert normalize_sql(actual_query) == normalize_sql(expected_query)
            mock_insert.assert_called_once()
          
def test_get_wishlist(db: SteamDatabase):
    with patch.object(db, '_check_table_item', return_value=True):
        db.cur.fetchall.return_value = test_data.DB_WISHLIST_RESPONSE
        wishlist = db.get_wishlist(test_data.STEAM_USER_ID)
        assert wishlist == test_data.DB_WISHLIST_PROCESSED
        
        # Verify _check_table_item was called with the correct parameters
        db._check_table_item.assert_called_once_with('steamid', 'users', test_data.STEAM_USER_ID)
        # 
        expected_query = f"""
            SELECT steamid, appid, priority FROM wishlist
            WHERE steamid = '{test_data.STEAM_USER_ID}';
        """
        
        # query being called within the method
        actual_query = db.cur.execute.call_args[0][0]
        assert normalize_sql(actual_query) == normalize_sql(expected_query)

def test_add_library(db: SteamDatabase):
    with patch.object(db, '_check_table_item', return_value=True):
        # mock insert row
        with patch.object(db, '_insert_new_row') as mock_insert:
            items = db.add_to_library(test_data.STEAM_USER_ID, test_data.CORRECT_LIBRARY_PROCESSED)
            assert items > 0
            
            # Verify _check_table_item was called with the correct parameters
            db._check_table_item.assert_called_once_with('steamid', 'users', test_data.STEAM_USER_ID)
            
            # check correct query was created
            expected_query = f"""
                ON CONFLICT (steamid, appid)
                DO UPDATE SET
                playtime_minutes = EXCLUDED.playtime_minutes
            """
            actual_query = mock_insert.call_args[0][3]
            assert normalize_sql(actual_query) == normalize_sql(expected_query)
            mock_insert.assert_called_once()
          
def test_get_library(db: SteamDatabase):
    with patch.object(db, '_check_table_item', return_value=True):
        db.cur.fetchall.return_value = test_data.DB_LIBRARY_RESPONSE
        library = db.get_library(test_data.STEAM_USER_ID)
        assert library == test_data.DB_LIBRARY_PROCESSED
        
        # Verify _check_table_item was called with the correct parameters
        db._check_table_item.assert_called_once_with('steamid', 'users', test_data.STEAM_USER_ID)
        # 
        expected_query = f"""
            SELECT steamid, appid, playtime_minutes FROM user_library
            WHERE steamid = '{test_data.STEAM_USER_ID}';
        """
        
        # query being called within the method
        actual_query = db.cur.execute.call_args[0][0]
        assert normalize_sql(actual_query) == normalize_sql(expected_query)
        
        
def normalize_sql(query):
    # Remove extra whitespace, newlines, and indentation
    return ' '.join(query.split())