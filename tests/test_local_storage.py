import pytest
import psycopg2 as pg2
import logging
import json
import os
from unittest.mock import patch, mock_open

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
    
@patch("src.tools.local_storage.parse_payment_history_steam")    
def test_parse_library_purchase_history(mock_history, create_html_steam_file):
    mock_history.return_value = TEST_HTML_STEAM_DATA
    actual_values = local_storage.parse_library_purchase_history("../data")
    assert TEST_HTML_STEAM_DATA == actual_values
    
def test_parse_payment_history_steam(create_html_steam_file):
    actual_values = local_storage.parse_payment_history_steam(FILE_PATH_HTML)
    assert TEST_HTML_STEAM_DATA == actual_values

@pytest.fixture
def create_html_kinguin_file():
    with open(FILE_PATH_HTML, 'w', encoding='utf-8') as file:
        file.write(HTML_KINGUIN_DATA)   
    yield
    os.remove(FILE_PATH_HTML)    
    
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
TEST_HTML_STEAM_DATA = [
    {"name": "INSIDE", "price": 199},
    {"name": "Project Warlock", "price": 240},
    {"name": "The Inheritance of Crimson Manor", "price": 399}
]

HTML_KINGUIN_DATA = """
<tr class="sc-fIITEw lbZwmo"><td colspan="8" class="sc-lheXJl gBFfCM"><div class="sc-cqJhZP fWXLdX"><div class="sc-jNHqnW dlRnPv"><div class="sc-eSxRXt daPkwT"><button type="button"><span>Order details</span><svg aria-hidden="true" focusable="false" data-prefix="fal" data-icon="circle-chevron-up" class="svg-inline--fa fa-circle-chevron-up " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256s256-114.6 256-256S397.4 0 256 0zM256 480c-123.5 0-224-100.5-224-224s100.5-224 224-224s224 100.5 224 224S379.5 480 256 480zM267.3 164.7C264.2 161.6 260.1 160 256 160S247.8 161.6 244.7 164.7l-112 112c-6.25 6.25-6.25 16.38 0 22.62s16.38 6.25 22.62 0L256 198.6l100.7 100.7c6.25 6.25 16.38 6.25 22.62 0s6.25-16.38 0-22.62L267.3 164.7z"></path></svg></button></div><div class="sc-cAhXWc gjJyzv"><button type="button" class="sc-gsFzgR jQlHDY"><svg aria-hidden="true" focusable="false" data-prefix="fal" data-icon="ellipsis-vertical" class="svg-inline--fa fa-ellipsis-vertical " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 512"><path fill="currentColor" d="M64 384C81.67 384 96 398.3 96 416C96 433.7 81.67 448 64 448C46.33 448 32 433.7 32 416C32 398.3 46.33 384 64 384zM64 224C81.67 224 96 238.3 96 256C96 273.7 81.67 288 64 288C46.33 288 32 273.7 32 256C32 238.3 46.33 224 64 224zM64 128C46.33 128 32 113.7 32 96C32 78.33 46.33 64 64 64C81.67 64 96 78.33 96 96C96 113.7 81.67 128 64 128z"></path></svg></button><div class="sc-gqtqkP finqZU"><ul><li><button type="button"><svg aria-hidden="true" focusable="false" data-prefix="fal" data-icon="file-arrow-down" class="svg-inline--fa fa-file-arrow-down fa-fw " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="currentColor" d="M365.3 125.3l-106.5-106.5C246.7 6.742 230.5 0 213.5 0H64C28.65 0 0 28.65 0 64l.0065 384c0 35.35 28.65 64 64 64H320c35.35 0 64-28.65 64-64V170.5C384 153.5 377.3 137.3 365.3 125.3zM224 34.08c4.477 1.566 8.666 3.846 12.12 7.299l106.5 106.5C346.1 151.3 348.4 155.5 349.9 160H240C231.2 160 224 152.8 224 144V34.08zM352 448c0 17.64-14.36 32-32 32H64c-17.64 0-32-14.36-32-32V64c0-17.64 14.36-32 32-32h128v112C192 170.5 213.5 192 240 192H352V448zM208 240C208 231.2 200.8 224 192 224S176 231.2 176 240v121.4L123.3 308.7C120.2 305.6 116.1 304 112 304S103.8 305.6 100.7 308.7c-6.25 6.25-6.25 16.38 0 22.62l80 80c6.25 6.25 16.38 6.25 22.62 0l80-80c6.25-6.25 6.25-16.38 0-22.62s-16.38-6.25-22.62 0L208 361.4V240z"></path></svg><span>Download keys</span></button></li><li><button type="button"><svg aria-hidden="true" focusable="false" data-prefix="fal" data-icon="cart-plus" class="svg-inline--fa fa-cart-plus fa-fw " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M240 160C240 151.2 247.2 144 256 144H304V96C304 87.16 311.2 80 320 80C328.8 80 336 87.16 336 96V144H384C392.8 144 400 151.2 400 160C400 168.8 392.8 176 384 176H336V224C336 232.8 328.8 240 320 240C311.2 240 304 232.8 304 224V176H256C247.2 176 240 168.8 240 160zM80 0C87.47 0 93.95 5.17 95.6 12.45L100 32H541.8C562.1 32 578.3 52.25 572.6 72.66L518.6 264.7C514.7 278.5 502.1 288 487.8 288H158.2L172.8 352H496C504.8 352 512 359.2 512 368C512 376.8 504.8 384 496 384H160C152.5 384 146.1 378.8 144.4 371.5L67.23 32H16C7.164 32 0 24.84 0 16C0 7.164 7.164 0 16 0H80zM107.3 64L150.1 256H487.8L541.8 64H107.3zM128 456C128 425.1 153.1 400 184 400C214.9 400 240 425.1 240 456C240 486.9 214.9 512 184 512C153.1 512 128 486.9 128 456zM184 480C197.3 480 208 469.3 208 456C208 442.7 197.3 432 184 432C170.7 432 160 442.7 160 456C160 469.3 170.7 480 184 480zM512 456C512 486.9 486.9 512 456 512C425.1 512 400 486.9 400 456C400 425.1 425.1 400 456 400C486.9 400 512 425.1 512 456zM456 432C442.7 432 432 442.7 432 456C432 469.3 442.7 480 456 480C469.3 480 480 469.3 480 456C480 442.7 469.3 432 456 432z"></path></svg><span>Order again</span></button></li></ul></div></div></div><div class="sc-jNHqnW hynrhk"><div class="sc-aaqME lcFIbe"><div class="sc-iRFsWr hSynhr"><span>Order ID</span></div><div class="sc-eZhRLC bFRzEd">JTBSYWVCWCF</div></div><div class="sc-aaqME lcFIbe"><div class="sc-iRFsWr hSynhr"><span>Date</span></div><div class="sc-eZhRLC cEMwzP"><time datetime="1665454413540">10-10-2022</time></div></div><div class="sc-aaqME lcFIbe"></div><div class="sc-aaqME lcFIbe"></div><div class="sc-dYtuZ fVbKZt"><div class="sc-iRFsWr hSynhr"><span>Order</span>: <span>Completed</span></div><div class="sc-eZhRLC gPOUuU"><span>Product is delivered. You can find your key in the <a target="_blank" href="https://www.kinguin.net/inventory/games">Inventory</a>. In case of any issues with the key, report the issue to the merchant. Go to Inventory, click "claim" or "show key" and click "report a key".</span></div></div></div><table class="sc-hAWBJg cYDEUP"><tr class="sc-jwQYvw hlGyez"><th class="sc-dMOJrz lfdjre"><span>From</span></th><th class="sc-dMOJrz gAcyMz"></th><th class="sc-dMOJrz gAcyMz"><span>Product name</span></th><th class="sc-dMOJrz gAcyMz"><span>Delivery type</span></th><th class="sc-dMOJrz gAcyMz"></th><th class="sc-dMOJrz gAcyMz"></th><th class="sc-dMOJrz gAcyMz"></th></tr><tr class="sc-jwQYvw hlGyez"><td class="sc-gFSQbh emltay">Zero</td><td class="sc-gFSQbh qqhMa">1 </td><td class="sc-gFSQbh isTTpv">Dead Space Origin CD Key</td><td class="sc-gFSQbh isTTpv"><div><span class="sc-juEPzu hGHSJl"><span>Inventory</span></span></div></td><td class="sc-gFSQbh isTTpv"><div class="sc-gDGHff bPODr"><span>Archived</span></div></td><td class="sc-gFSQbh fRcDTw"><span itemprop="priceCurrency" content="USD"></span><span class="" content="2.82">$2.82</span></td><td class="sc-gFSQbh XHsCE"><div class="sc-ljMRFG klCnMC"><button type="button"><svg aria-labelledby="svg-inline--fa-title-SGzCuj9XKQSs" data-prefix="fal" data-icon="cart-plus" class="svg-inline--fa fa-cart-plus " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><title id="svg-inline--fa-title-SGzCuj9XKQSs">Order again</title><path fill="currentColor" d="M240 160C240 151.2 247.2 144 256 144H304V96C304 87.16 311.2 80 320 80C328.8 80 336 87.16 336 96V144H384C392.8 144 400 151.2 400 160C400 168.8 392.8 176 384 176H336V224C336 232.8 328.8 240 320 240C311.2 240 304 232.8 304 224V176H256C247.2 176 240 168.8 240 160zM80 0C87.47 0 93.95 5.17 95.6 12.45L100 32H541.8C562.1 32 578.3 52.25 572.6 72.66L518.6 264.7C514.7 278.5 502.1 288 487.8 288H158.2L172.8 352H496C504.8 352 512 359.2 512 368C512 376.8 504.8 384 496 384H160C152.5 384 146.1 378.8 144.4 371.5L67.23 32H16C7.164 32 0 24.84 0 16C0 7.164 7.164 0 16 0H80zM107.3 64L150.1 256H487.8L541.8 64H107.3zM128 456C128 425.1 153.1 400 184 400C214.9 400 240 425.1 240 456C240 486.9 214.9 512 184 512C153.1 512 128 486.9 128 456zM184 480C197.3 480 208 469.3 208 456C208 442.7 197.3 432 184 432C170.7 432 160 442.7 160 456C160 469.3 170.7 480 184 480zM512 456C512 486.9 486.9 512 456 512C425.1 512 400 486.9 400 456C400 425.1 425.1 400 456 400C486.9 400 512 425.1 512 456zM456 432C442.7 432 432 442.7 432 456C432 469.3 442.7 480 456 480C469.3 480 480 469.3 480 456C480 442.7 469.3 432 456 432z"></path></svg></button><button type="button"><svg aria-labelledby="svg-inline--fa-title-zdetWZeuE1Td" data-prefix="fal" data-icon="file-arrow-down" class="svg-inline--fa fa-file-arrow-down " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><title id="svg-inline--fa-title-zdetWZeuE1Td">Download keys</title><path fill="currentColor" d="M365.3 125.3l-106.5-106.5C246.7 6.742 230.5 0 213.5 0H64C28.65 0 0 28.65 0 64l.0065 384c0 35.35 28.65 64 64 64H320c35.35 0 64-28.65 64-64V170.5C384 153.5 377.3 137.3 365.3 125.3zM224 34.08c4.477 1.566 8.666 3.846 12.12 7.299l106.5 106.5C346.1 151.3 348.4 155.5 349.9 160H240C231.2 160 224 152.8 224 144V34.08zM352 448c0 17.64-14.36 32-32 32H64c-17.64 0-32-14.36-32-32V64c0-17.64 14.36-32 32-32h128v112C192 170.5 213.5 192 240 192H352V448zM208 240C208 231.2 200.8 224 192 224S176 231.2 176 240v121.4L123.3 308.7C120.2 305.6 116.1 304 112 304S103.8 305.6 100.7 308.7c-6.25 6.25-6.25 16.38 0 22.62l80 80c6.25 6.25 16.38 6.25 22.62 0l80-80c6.25-6.25 6.25-16.38 0-22.62s-16.38-6.25-22.62 0L208 361.4V240z"></path></svg></button></div></td></tr><tr class="sc-jwQYvw hlGyez"><td class="sc-gFSQbh emltay">Green Keys</td><td class="sc-gFSQbh qqhMa">1 </td><td class="sc-gFSQbh isTTpv">Dead Space 2 Origin CD Key</td><td class="sc-gFSQbh isTTpv"><div><span class="sc-juEPzu hGHSJl"><span>Inventory</span></span></div></td><td class="sc-gFSQbh isTTpv"><div class="sc-gDGHff bPODr"><span>Archived</span></div></td><td class="sc-gFSQbh fRcDTw"><span itemprop="priceCurrency" content="USD"></span><span class="" content="5.14">$5.14</span></td><td class="sc-gFSQbh XHsCE"><div class="sc-ljMRFG klCnMC"><button type="button"><svg aria-labelledby="svg-inline--fa-title-bA6e2kkFGftD" data-prefix="fal" data-icon="cart-plus" class="svg-inline--fa fa-cart-plus " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><title id="svg-inline--fa-title-bA6e2kkFGftD">Order again</title><path fill="currentColor" d="M240 160C240 151.2 247.2 144 256 144H304V96C304 87.16 311.2 80 320 80C328.8 80 336 87.16 336 96V144H384C392.8 144 400 151.2 400 160C400 168.8 392.8 176 384 176H336V224C336 232.8 328.8 240 320 240C311.2 240 304 232.8 304 224V176H256C247.2 176 240 168.8 240 160zM80 0C87.47 0 93.95 5.17 95.6 12.45L100 32H541.8C562.1 32 578.3 52.25 572.6 72.66L518.6 264.7C514.7 278.5 502.1 288 487.8 288H158.2L172.8 352H496C504.8 352 512 359.2 512 368C512 376.8 504.8 384 496 384H160C152.5 384 146.1 378.8 144.4 371.5L67.23 32H16C7.164 32 0 24.84 0 16C0 7.164 7.164 0 16 0H80zM107.3 64L150.1 256H487.8L541.8 64H107.3zM128 456C128 425.1 153.1 400 184 400C214.9 400 240 425.1 240 456C240 486.9 214.9 512 184 512C153.1 512 128 486.9 128 456zM184 480C197.3 480 208 469.3 208 456C208 442.7 197.3 432 184 432C170.7 432 160 442.7 160 456C160 469.3 170.7 480 184 480zM512 456C512 486.9 486.9 512 456 512C425.1 512 400 486.9 400 456C400 425.1 425.1 400 456 400C486.9 400 512 425.1 512 456zM456 432C442.7 432 432 442.7 432 456C432 469.3 442.7 480 456 480C469.3 480 480 469.3 480 456C480 442.7 469.3 432 456 432z"></path></svg></button><button type="button"><svg aria-labelledby="svg-inline--fa-title-0tmLiIN31u4X" data-prefix="fal" data-icon="file-arrow-down" class="svg-inline--fa fa-file-arrow-down " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><title id="svg-inline--fa-title-0tmLiIN31u4X">Download keys</title><path fill="currentColor" d="M365.3 125.3l-106.5-106.5C246.7 6.742 230.5 0 213.5 0H64C28.65 0 0 28.65 0 64l.0065 384c0 35.35 28.65 64 64 64H320c35.35 0 64-28.65 64-64V170.5C384 153.5 377.3 137.3 365.3 125.3zM224 34.08c4.477 1.566 8.666 3.846 12.12 7.299l106.5 106.5C346.1 151.3 348.4 155.5 349.9 160H240C231.2 160 224 152.8 224 144V34.08zM352 448c0 17.64-14.36 32-32 32H64c-17.64 0-32-14.36-32-32V64c0-17.64 14.36-32 32-32h128v112C192 170.5 213.5 192 240 192H352V448zM208 240C208 231.2 200.8 224 192 224S176 231.2 176 240v121.4L123.3 308.7C120.2 305.6 116.1 304 112 304S103.8 305.6 100.7 308.7c-6.25 6.25-6.25 16.38 0 22.62l80 80c6.25 6.25 16.38 6.25 22.62 0l80-80c6.25-6.25 6.25-16.38 0-22.62s-16.38-6.25-22.62 0L208 361.4V240z"></path></svg></button></div></td></tr><tr class="sc-jwQYvw hlGyez"><td class="sc-gFSQbh emltay">Green Keys</td><td class="sc-gFSQbh qqhMa">1 </td><td class="sc-gFSQbh isTTpv">Dead Space 3 EA Origin CD Key</td><td class="sc-gFSQbh isTTpv"><div><span class="sc-juEPzu hGHSJl"><span>Inventory</span></span></div></td><td class="sc-gFSQbh isTTpv"><div class="sc-gDGHff bPODr"><span>Archived</span></div></td><td class="sc-gFSQbh fRcDTw"><span itemprop="priceCurrency" content="USD"></span><span class="" content="7.49">$7.49</span></td><td class="sc-gFSQbh XHsCE"><div class="sc-ljMRFG klCnMC"><button type="button"><svg aria-labelledby="svg-inline--fa-title-IHAFlJ9HMg4P" data-prefix="fal" data-icon="cart-plus" class="svg-inline--fa fa-cart-plus " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><title id="svg-inline--fa-title-IHAFlJ9HMg4P">Order again</title><path fill="currentColor" d="M240 160C240 151.2 247.2 144 256 144H304V96C304 87.16 311.2 80 320 80C328.8 80 336 87.16 336 96V144H384C392.8 144 400 151.2 400 160C400 168.8 392.8 176 384 176H336V224C336 232.8 328.8 240 320 240C311.2 240 304 232.8 304 224V176H256C247.2 176 240 168.8 240 160zM80 0C87.47 0 93.95 5.17 95.6 12.45L100 32H541.8C562.1 32 578.3 52.25 572.6 72.66L518.6 264.7C514.7 278.5 502.1 288 487.8 288H158.2L172.8 352H496C504.8 352 512 359.2 512 368C512 376.8 504.8 384 496 384H160C152.5 384 146.1 378.8 144.4 371.5L67.23 32H16C7.164 32 0 24.84 0 16C0 7.164 7.164 0 16 0H80zM107.3 64L150.1 256H487.8L541.8 64H107.3zM128 456C128 425.1 153.1 400 184 400C214.9 400 240 425.1 240 456C240 486.9 214.9 512 184 512C153.1 512 128 486.9 128 456zM184 480C197.3 480 208 469.3 208 456C208 442.7 197.3 432 184 432C170.7 432 160 442.7 160 456C160 469.3 170.7 480 184 480zM512 456C512 486.9 486.9 512 456 512C425.1 512 400 486.9 400 456C400 425.1 425.1 400 456 400C486.9 400 512 425.1 512 456zM456 432C442.7 432 432 442.7 432 456C432 469.3 442.7 480 456 480C469.3 480 480 469.3 480 456C480 442.7 469.3 432 456 432z"></path></svg></button><button type="button"><svg aria-labelledby="svg-inline--fa-title-3HVYa49vwTnV" data-prefix="fal" data-icon="file-arrow-down" class="svg-inline--fa fa-file-arrow-down " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><title id="svg-inline--fa-title-3HVYa49vwTnV">Download keys</title><path fill="currentColor" d="M365.3 125.3l-106.5-106.5C246.7 6.742 230.5 0 213.5 0H64C28.65 0 0 28.65 0 64l.0065 384c0 35.35 28.65 64 64 64H320c35.35 0 64-28.65 64-64V170.5C384 153.5 377.3 137.3 365.3 125.3zM224 34.08c4.477 1.566 8.666 3.846 12.12 7.299l106.5 106.5C346.1 151.3 348.4 155.5 349.9 160H240C231.2 160 224 152.8 224 144V34.08zM352 448c0 17.64-14.36 32-32 32H64c-17.64 0-32-14.36-32-32V64c0-17.64 14.36-32 32-32h128v112C192 170.5 213.5 192 240 192H352V448zM208 240C208 231.2 200.8 224 192 224S176 231.2 176 240v121.4L123.3 308.7C120.2 305.6 116.1 304 112 304S103.8 305.6 100.7 308.7c-6.25 6.25-6.25 16.38 0 22.62l80 80c6.25 6.25 16.38 6.25 22.62 0l80-80c6.25-6.25 6.25-16.38 0-22.62s-16.38-6.25-22.62 0L208 361.4V240z"></path></svg></button></div></td></tr><tr class="sc-jwQYvw iwyXuk"><td class="sc-gFSQbh isTTpv"></td><td class="sc-gFSQbh isTTpv"></td><td class="sc-gFSQbh isTTpv"></td><td class="sc-gFSQbh isTTpv"></td><td class="sc-gFSQbh ekUIti"></td><td class="sc-gFSQbh ekUIti"></td><td class="sc-gFSQbh isTTpv"></td><td class="sc-gFSQbh isTTpv"></td></tr></table><table class="sc-hAWBJg cYDEUP" style="margin-top: 1rem;"><tr class="sc-jwQYvw hlGyez"><th class="sc-dMOJrz lfdjre"></th><th class="sc-dMOJrz gAcyMz"></th><th class="sc-dMOJrz gAcyMz"></th><th class="sc-dMOJrz gAcyMz"></th><th class="sc-dMOJrz gAcyMz"></th></tr><tr class="sc-jwQYvw htOAec"><td class="sc-gFSQbh xDlHP"></td><td class="sc-gFSQbh isTTpv"></td><td class="sc-gFSQbh isTTpv"></td><td class="sc-gFSQbh isTTpv"></td><td colspan="2" class="sc-gFSQbh isTTpv"><div class="sc-iLOkMM gRxlRV"><div class="sc-fUQcsx htPCxd"><div class="sc-iJCbQK jRxSiW"><span>Grand total</span></div><div class="sc-fSDTwv dZePLz"><span itemprop="priceCurrency" content="USD"></span><span class="" content="18.01">$18.01</span></div></div></div></td><td class="sc-gFSQbh isTTpv"></td></tr></table></div></td></tr>
"""
TEST_HTML_KINGUIN_DATA = [
    {"name": "Dead Space", "price": 282},
    {"name": "Dead Space 2", "price": 514},
    {"name": "Dead Space 3", "price": 749}
]