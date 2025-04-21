import pytest
import psycopg2 as pg2
import logging
import json
import os
from unittest.mock import patch, mock_open

from src.tools.local_storage import check_file, load_from_json, save_to_json, remove_items, delete_file

FILE_PATH="../data/temp_data.json"

@pytest.fixture
def create_file():
    data_to_save = {
        "data": TEST_DATA
    }
    with open(FILE_PATH, 'w') as json_file:
        json.dump(data_to_save, json_file, indent=2)
        
@patch('builtins.open')
@patch('json.dump')
@patch('src.tools.local_storage.logger.info')
def test_save_to_json(mock_log, mock_json_dump, mock_open):
    save_to_json(FILE_PATH, TEST_DATA)
    mock_open.assert_called_once_with(FILE_PATH, 'w')
    
    mock_file = mock_open.return_value.__enter__.return_value
    mock_json_dump.assert_called_once_with(TEST_DATA, mock_file, indent=4)
    
    expected_log  = f"Data saved to {FILE_PATH}"
    mock_log.assert_called_once_with(expected_log)

def test_save_to_json_file():
    save_to_json(FILE_PATH, TEST_DATA)
        
    with open(FILE_PATH, 'r') as f:
        saved_data = json.load(f)
    assert saved_data == {"data": TEST_DATA}
    
    os.remove(FILE_PATH)
     
@patch('json.load') 
@patch('builtins.open')
@patch('src.tools.local_storage.logger.info')
def test_save_to_json(mock_log, mock_open, json_load):
    load_from_json(FILE_PATH)
    mock_open.assert_called_once_with(FILE_PATH, 'r')
    
    expected_log  = f"Data loaded from {FILE_PATH}"
    mock_log.assert_called_once_with(expected_log)

def test_load_from_json_file(create_file):
    json_data = load_from_json(FILE_PATH)
    assert json_data == {"data": TEST_DATA}
    
    os.remove(FILE_PATH)

def test_delete_file(create_file):
    delete_file(FILE_PATH)
    assert not os.path.exists(FILE_PATH)
        

def test_check_file(create_file):
    file_exist = check_file(FILE_PATH)
    assert file_exist
    
    os.remove(FILE_PATH)

def test_remove_items():
    all_items = [1,2,3,4,5,6,7,8,9,10]
    subset = [1,4,8,12]
    update_list = remove_items(all_items, subset)
    
    assert update_list == [2,3,5,6,7,9,10]
    
    
# ----------------------------
# ------  WISHLIST DATA ------
# ----------------------------
TEST_DATA = {"unique": [], "games": []}