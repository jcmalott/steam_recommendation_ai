import pytest
import psycopg2 as pg2
import logging
import json
import os
from unittest.mock import patch, mock_open, call

import src.tools.local_storage as local_storage

FILE_PATH_JSON="../data/temp_data.json"
FILE_PATH_HTML="../data/temp_data.html"

@pytest.fixture
def create_json_file():
    data_to_save = {
        "data": TEST_DATA
    }
    with open(FILE_PATH_JSON, 'w') as json_file:
        json.dump(data_to_save, json_file, indent=2)
        
@patch('builtins.open')
@patch('json.dump')
@patch('src.tools.local_storage.logger.info')
def test_save_to_json(mock_log, mock_json_dump, mock_open):
    local_storage.save_to_json(FILE_PATH_JSON, TEST_DATA)
    mock_open.assert_called_once_with(FILE_PATH_JSON, 'w')
    
    mock_file = mock_open.return_value.__enter__.return_value
    mock_json_dump.assert_called_once_with(TEST_DATA, mock_file, indent=4)
    
    expected_log  = f"Data saved to {FILE_PATH_JSON}"
    mock_log.assert_called_once_with(expected_log)

def test_save_to_json_file():
    local_storage.save_to_json(FILE_PATH_JSON, TEST_DATA)
        
    with open(FILE_PATH_JSON, 'r') as f:
        saved_data = json.load(f)
    assert saved_data == {"data": TEST_DATA}
    
    os.remove(FILE_PATH_JSON)
     
@patch('json.load') 
@patch('builtins.open')
@patch('src.tools.local_storage.logger.info')
def test_save_to_json(mock_log, mock_open, json_load):
    local_storage.load_from_json(FILE_PATH_JSON)
    mock_open.assert_called_once_with(FILE_PATH_JSON, 'r')
    
    expected_log  = f"Data loaded from {FILE_PATH_JSON}"
    mock_log.assert_called_once_with(expected_log)

def test_load_from_json_file(create_json_file):
    json_data = local_storage.load_from_json(FILE_PATH_JSON)
    assert json_data == {"data": TEST_DATA}
    
    os.remove(FILE_PATH_JSON)

def test_delete_file(create_json_file):
    local_storage.delete_file(FILE_PATH_JSON)
    assert not os.path.exists(FILE_PATH_JSON)
        

def test_check_file(create_json_file):
    file_exist = local_storage.check_file(FILE_PATH_JSON)
    assert file_exist
    
    os.remove(FILE_PATH_JSON)

def test_remove_items():
    all_items = [1,2,3,4,5,6,7,8,9,10]
    subset = [1,4,8,12]
    update_list = local_storage.remove_items(all_items, subset)
    
    assert update_list == [2,3,5,6,7,9,10]

@pytest.fixture
def create_html_steam_file():
    with open(FILE_PATH_HTML, 'w', encoding='utf-8') as file:
        file.write(HTML_STEAM_DATA)   
    yield
    os.remove(FILE_PATH_HTML)
    
@pytest.fixture
def create_html_kinguin_file():
    with open(FILE_PATH_HTML, 'w', encoding='utf-8') as file:
        file.write(HTML_KINGUIN_DATA)   
    yield
    os.remove(FILE_PATH_HTML)  

# multiple files
# wrong path
# no files
TEST_HTML_STEAM_DATA = [
    {"game_name": "INSIDE", "price": 199},
    {"game_name": "Project Warlock", "price": 240},
    {"game_name": "The Inheritance of Crimson Manor", "price": 399}
]
TEST_HTML_KINGUIN_DATA = [
    {"game_name": "Dead Space", "price": 282},
    {"game_name": "Dead Space 2", "price": 514},
    {"game_name": "Dead Space 3", "price": 749}
]
test_cases=[
    ("../data/purchase_history/steam", "parse_payment_history_steam", TEST_HTML_STEAM_DATA, TEST_HTML_STEAM_DATA, ["file1.html"]),
    ("../data/purchase_history/steam", "parse_payment_history_steam", TEST_HTML_STEAM_DATA, (TEST_HTML_STEAM_DATA+TEST_HTML_STEAM_DATA), ["file1.html", "file2.html"]),
    ("../data/purchase_history/kinguin", "parse_payment_history_kinguin", TEST_HTML_KINGUIN_DATA, TEST_HTML_KINGUIN_DATA, ["file1.html"])
]
@patch("os.path.isdir", return_value=True)
@patch("os.listdir")
@patch("os.path.join", side_effect=os.path.join)
@pytest.mark.parametrize('dir_path, func, func_return, result, files', test_cases)
def test_parse_library_purchase_history_steam(mock_join, mock_listdir, mock_isdir, func, dir_path, func_return, result, files):
    mock_listdir.return_value=files
    with patch.object(local_storage, func, return_value=func_return) as mock_parser:
        actual_values = local_storage.parse_library_purchase_history(dir_path)
        assert result == actual_values
    
        mock_isdir.assert_called_once_with(dir_path)
        mock_listdir.assert_called_once_with(dir_path)
        
        # Verify the correct number of calls to the parser
        assert mock_parser.call_count == len(files)
        
        # The path.join should be called for each HTML file
        calls = [call(os.path.join(dir_path, file)) for file in files]
        mock_parser.assert_has_calls(calls, any_order=True)
        
@patch("os.path.isdir")
@patch("os.listdir")
@patch("os.path.join", side_effect=os.path.join)
@pytest.mark.parametrize('dir_path, isdir, files, result', [
    ('../data/purchase_history/steam', False, ["file1.html"], None),
    ('../data/purchase_history/steam', True, [], None),
    ('../data/purchase_history/incorrect', True, ["file1.html"], None)
]) 
def test_parse_library_purchase_history_error(mock_join, mock_listdir, mock_isdir, dir_path, isdir, files, result):
    mock_isdir.return_value=isdir
    mock_listdir.return_value=files
    
    actual_values = local_storage.parse_library_purchase_history(dir_path)
    assert result == actual_values
    
def test_parse_payment_history_steam(create_html_steam_file):
    actual_values = local_storage.parse_payment_history_steam(FILE_PATH_HTML)
    assert TEST_HTML_STEAM_DATA == actual_values  
    
def test_parse_payment_history_kinguin(create_html_kinguin_file):
    actual_values = local_storage.parse_payment_history_kinguin(FILE_PATH_HTML)
    assert TEST_HTML_KINGUIN_DATA == actual_values
 
# ----------------------------
# ------  WISHLIST DATA ------
# ----------------------------
TEST_DATA = {"unique": [], "games": []}
HTML_STEAM_DATA = """
<div class="help_purchase_detail_box help_purchase_package ">
	<div class="purchase_date">Purchased: Apr 16, 2024 @ 3:26pm</div>

	<div class="purchase_line_items">
			<div class="">
				<span class="purchase_detail_field">INSIDE</span><span> - </span><span class="refund_value"><span>$1.99</span></span>
			</div>
			<div class="">
				<span class="purchase_detail_field">Project Warlock</span><span> - </span><span class="refund_value"><span>$2.40</span></span>
			</div>
			<div class="">
				<span class="purchase_detail_field">The Inheritance of Crimson Manor</span><span> - </span><span class="refund_value"><span>$3.99</span></span>
			</div>
	</div>
    <table class="purchase_totals">
        <tbody><tr>
            <td class="purchase_total_header">Subtotal</td>
            <td class="refund_value"><span>$51.98</span></td>
            <td></td>
        </tr>
                                        <tr>
                <td class="purchase_total_header">Discount</td>
                <td class="refund_value"><span>-$43.60</span></td>
                <td class="refund_value_details"><span>(-83%)</span></td>
            </tr>             
                <tr>
            <td colspan="3" class="line_break"></td>
        </tr>
        <tr>
            <td class="purchase_total_header">Total</td>
            <td class="refund_value"><span>$8.38</span></td>
            <td></td>
        </tr>
        </tbody>
    </table>
</div>
<div class="help_section_text" style="margin-top: 20px">Which product are you having trouble with?</div>
"""

HTML_KINGUIN_DATA = """
<tr class="sc-jwQYvw hlGyez"><td class="sc-gFSQbh emltay">Zero</td><td class="sc-gFSQbh qqhMa">1 </td><td class="sc-gFSQbh isTTpv">Dead Space Origin CD Key</td><td class="sc-gFSQbh isTTpv"><div><span class="sc-juEPzu hGHSJl"><span>Inventory</span></span></div></td><td class="sc-gFSQbh isTTpv"><div class="sc-gDGHff bPODr"><span>Archived</span></div></td><td class="sc-gFSQbh fRcDTw"><span itemprop="priceCurrency" content="USD"></span><span class="" content="2.82">$2.82</span></td></tr>

<tr class="sc-jwQYvw hlGyez"><td class="sc-gFSQbh emltay">Green Keys</td><td class="sc-gFSQbh qqhMa">1 </td><td class="sc-gFSQbh isTTpv">Dead Space 2 Origin CD Key</td><td class="sc-gFSQbh isTTpv"><div><span class="sc-juEPzu hGHSJl"><span>Inventory</span></span></div></td><td class="sc-gFSQbh isTTpv"><div class="sc-gDGHff bPODr"><span>Archived</span></div></td><td class="sc-gFSQbh fRcDTw"><span itemprop="priceCurrency" content="USD"></span><span class="" content="5.14">$5.14</span></td></tr>

<tr class="sc-jwQYvw hlGyez"><td class="sc-gFSQbh emltay">Green Keys</td><td class="sc-gFSQbh qqhMa">1 </td><td class="sc-gFSQbh isTTpv">Dead Space 3 EA Origin CD Key</td><td class="sc-gFSQbh isTTpv"><div><span class="sc-juEPzu hGHSJl"><span>Inventory</span></span></div></td><td class="sc-gFSQbh isTTpv"><div class="sc-gDGHff bPODr"><span>Archived</span></div></td><td class="sc-gFSQbh fRcDTw"><span itemprop="priceCurrency" content="USD"></span><span class="" content="7.49">$7.49</span></td>
"""