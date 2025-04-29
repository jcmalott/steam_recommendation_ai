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

def test_add_to_database(db: SteamDatabase):
    with patch.object(db, '_check_table_item', return_value=True):
        on_conflict = f"""
            ON CONFLICT (appid)
            DO UPDATE SET
                is_free = EXCLUDED.is_free,
                recommendations = EXCLUDED.recommendations
        """   
        fields = ['appid','game_type', 'game_name', 'is_free', 'detailed_description','header_image','website','recommendations','release_date','esrb_rating']
        table = 'games'
        result = db._add_to_database(test_data.STEAM_USER_ID, [test_data.CORRECT_GAME_PROCESSED], on_conflict, fields, table)
        assert result > 0    
        
def test_insert_new_row_success(db: SteamDatabase):
    """Test _insert_new_row with a successful insertion."""
    fields = ['appid','game_type']
    table = 'games'
    
    result = db._insert_new_row(table, fields,  [test_data.CORRECT_GAME_PROCESSED])
    assert result == True
    
    # Verify execute was called with the correct query and parameters
    expected_query = """
        INSERT INTO games (appid, game_type)
        VALUES (%s, %s)
    """
    actual_query = db.cur.executemany.call_args[0][0]
    assert normalize_sql(actual_query) == normalize_sql(expected_query) 
    
    # db.cur.executemany.assert_called_once_with(expected_query, [[1144200, "game"]])
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

add_to_library_conflict = f"""
    ON CONFLICT (steamid, appid)
    DO UPDATE SET
    playtime_minutes = EXCLUDED.playtime_minutes
""" 
add_to_wishlist_conflict = f"""
    ON CONFLICT (steamid, appid)
    DO UPDATE SET
    priority = EXCLUDED.priority
"""
@pytest.mark.parametrize('func_name, on_conflict, data', [
    ('add_to_library', add_to_library_conflict, test_data.CORRECT_LIBRARY_PROCESSED),
    ('add_to_wishlist', add_to_wishlist_conflict, test_data.WISHLIST)
])
def test_add_appids_to_db(db: SteamDatabase, func_name, on_conflict, data):
    db_func = getattr(db, func_name)
    
    with patch.object(db,'_check_table_item', return_value=True):
        with patch.object(db, '_insert_new_row') as mock_insert:
            # place function
            result = db_func(test_data.STEAM_USER_ID, data)
            assert result > 0 
            
            # Verify _check_table_item was called with the correct parameters
            db._check_table_item.assert_called_once_with('steamid', 'users', test_data.STEAM_USER_ID)
            
            # on_conflict 
            actual_query = mock_insert.call_args[0][3]
            assert normalize_sql(actual_query) == normalize_sql(on_conflict) 
            mock_insert.assert_called_once()     

add_to_games_conflict = f"""
    ON CONFLICT (appid)
    DO UPDATE SET
        is_free = EXCLUDED.is_free,
        recommendations = EXCLUDED.recommendations
"""  
add_to_developers_conflict = f"""
    ON CONFLICT (appid, developer_name)
    DO NOTHING
"""   
add_to_categories_conflict = f"""
    ON CONFLICT (appid, category_name)
    DO NOTHING
"""   
add_to_genres_conflict = f"""
    ON CONFLICT (appid, genre_name)
    DO NOTHING
"""  
add_to_prices_conflict = f"""
    ON CONFLICT (appid)
    DO UPDATE SET
        currency = EXCLUDED.currency,
        price_in_cents = EXCLUDED.price_in_cents,
        final_formatted = EXCLUDED.final_formatted,
        discount_percentage = EXCLUDED.discount_percentage
"""   
add_to_metacritic_conflict = f"""
    ON CONFLICT (appid)
    DO UPDATE SET
        score = EXCLUDED.score
""" 
add_to_publishers_conflict = f"""
    ON CONFLICT (appid, publisher_name)
    DO NOTHING
"""   
@patch.object(SteamDatabase,'_check_table_item', return_value=True)
@patch.object(SteamDatabase,'_insert_new_row', return_value=True)
@pytest.mark.parametrize('func_name, table, fields, data, on_conflict', [
    (
        'add_to_games', 
        'games',
        ['appid','game_type', 'game_name', 'is_free', 'detailed_description','header_image','website','recommendations','release_date','esrb_rating'],
        [test_data.CORRECT_GAME_PROCESSED],
        add_to_games_conflict
    ),
    (
        'add_to_developers', 
        'developers',
        ['appid','developer_name'],
        test_data.CORRECT_DEVELOPERS_PROCESSED,
        add_to_developers_conflict
    ),
    (
        'add_to_publishers', 
        'publishers',
        ['appid','publisher_name'],
        test_data.CORRECT_PUBLISHERS_PROCESSED,
        add_to_publishers_conflict
    ),
    (
        'add_to_categories', 
        'categories',
        ['appid','category_name'],
        test_data.CORRECT_CATEGORIES_PROCESSED,
        add_to_categories_conflict
    ),
    (
        'add_to_genres', 
        'genres',
        ['appid','genre_name'],
        test_data.CORRECT_GENRES_PROCESSED,
        add_to_genres_conflict
    ),
    (   
        'add_to_prices', 
        'prices',
        ['appid','currency','price_in_cents','final_formatted','discount_percentage'],
        test_data.CORRECT_PRICES_PROCESSED,
        add_to_prices_conflict
    ),
    (
        'add_to_metacritic', 
        'metacritic',
        ['appid','score','url'],
        test_data.CORRECT_META_PROCESSED,
        add_to_metacritic_conflict
    )
])
def test_add_to_db(mock_insert, mock_table, db: SteamDatabase, func_name, table, fields, data, on_conflict):
    db_func = getattr(db, func_name)
    
    result = db_func(test_data.STEAM_USER_ID, [test_data.CORRECT_GAME_PROCESSED])
    assert result > 0 
    
    # Verify _check_table_item was called with the correct parameters
    mock_table.assert_called_once_with('steamid', 'users', test_data.STEAM_USER_ID)

    mock_args = mock_insert.call_args[0]
    assert mock_args[0] == table
    assert mock_args[1] == fields
    assert mock_args[2] == data
    assert normalize_sql(mock_args[3]) == normalize_sql(on_conflict) 
    mock_insert.assert_called_once()  
    
@pytest.mark.parametrize('func_name, error_message', [
    ('add_to_developers', "'Database add_to_developers missing correct key'"),
    ('add_to_publishers', "'Database add_to_publishers missing correct key'"),
    ('add_to_categories', "'Database add_to_categories missing correct key'"),
    ( 'add_to_genres', "'Database add_to_genres missing correct key'"),
    ('add_to_prices', "'Database add_to_prices missing correct key'"),
    ('add_to_metacritic', "'Database add_to_metacritic missing correct key'")
])
def test_add_to_db_fail(db: SteamDatabase, func_name, error_message):
    db_func = getattr(db, func_name)
    
    with pytest.raises(KeyError) as excinfo:
        db_func(test_data.STEAM_USER_ID, [{'appid': 0, 'currency': "USD"}])
        
    #  Verify the exception has the expected message including the specific user ID
    assert str(excinfo.value) == error_message

get_library_query = f"""
    SELECT steamid, appid, playtime_minutes FROM user_library
    WHERE steamid = '{test_data.STEAM_USER_ID}';
"""
get_wishlist_query = f"""
    SELECT steamid, appid, priority FROM wishlist
    WHERE steamid = '{test_data.STEAM_USER_ID}';
"""
@pytest.mark.parametrize('func_name, response, processed, query', [
    ('get_library', test_data.DB_LIBRARY_RESPONSE, test_data.DB_LIBRARY_PROCESSED, get_library_query),
    ('get_wishlist', test_data.DB_WISHLIST_RESPONSE, test_data.DB_WISHLIST_PROCESSED, get_wishlist_query),
    ('get_games', test_data.DB_GAMES_RESPONSE, test_data.CORRECT_GAMES_PROCESSED, None),
    ('get_developers', test_data.DB_DEVELOPERS_RESPONSE, test_data.CORRECT_DEVELOPERS_PROCESSED, None),
    ('get_publishers', test_data.DB_PUBLISHERS_RESPONSE, test_data.CORRECT_PUBLISHERS_PROCESSED, None),
    ('get_categories', test_data.DB_CATEGORIES_RESPONSE, test_data.CORRECT_CATEGORIES_PROCESSED, None),
    ('get_genres', test_data.DB_GENRES_RESPONSE, test_data.CORRECT_GENRES_PROCESSED, None),
    ('get_prices', test_data.DB_PRICES_RESPONSE, test_data.CORRECT_PRICES_PROCESSED, None),
    ('get_metacritics', test_data.DB_META_RESPONSE, test_data.CORRECT_META_PROCESSED, None),
])
def test_get_user_appids(db: SteamDatabase, func_name, response, processed, query):
    db_func = getattr(db, func_name)
    
    with patch.object(db, '_check_table_item', return_value=True):
        db.cur.fetchall.return_value = response
        processed_response = db_func(test_data.STEAM_USER_ID)
        assert processed_response == processed
        
        # query being called within the method
        if query:
            actual_query = db.cur.execute.call_args[0][0]
            assert normalize_sql(actual_query) == normalize_sql(query)  

@pytest.mark.parametrize('items, actual_result', [
    ([839770, 878290, 881100], True),
    ([], False)
])           
def test_delete_entries(items, actual_result, db: SteamDatabase):
    result = db._delete_entries(test_data.STEAM_USER_ID, 'wishlist', items)
    assert result == actual_result
    
    if actual_result:
        appids = ', '.join(str(item) for item in items)
        query = f"""
            DELETE FROM wishlist
            WHERE steamid = '76561198041511379' AND appid IN ({appids})
        """
        actual_query = db.cur.execute.call_args[0][0]
        assert normalize_sql(actual_query) == normalize_sql(query)
        
        
def test_set_games_update_status(db: SteamDatabase):
    # Mock _check_table_item to return False (user doesn't exist)
    with patch.object(db, '_check_table_item', return_value=True):
        # Mock cursor.fetchone to return True (update needed)
        db.cur.fetchone.return_value = True
        result = db.set_games_update_status(test_data.STEAM_USER_ID)
        
        # Verify the result is True (update needed)
        assert result == True
        
        # Verify _check_table_item was called with the correct parameters
        db._check_table_item.assert_called_once_with('steamid', 'schedule_data_retrieval', test_data.STEAM_USER_ID)
        
        # Verify execute was called with the correct query
        expected_query = f"""
                UPDATE schedule_data_retrieval
                SET games_updated_at = NOW()
                WHERE steamid = '{test_data.STEAM_USER_ID}';
            """
            
        # query being called within the method
        actual_query = db.cur.execute.call_args[0][0]
        assert normalize_sql(actual_query) == normalize_sql(expected_query)
        
def normalize_sql(query):
    # Remove extra whitespace, newlines, and indentation
    return ' '.join(query.split())