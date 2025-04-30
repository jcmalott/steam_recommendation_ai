import json
from src import logger
import os
from bs4 import BeautifulSoup
from typing import List, Any, Dict
        
def save_to_json(file_path: str, variable_data: List):
    """
        Saves the current time and variable data to a JSON file
        
        filename: Path to the JSON file
        variable_data: Any JSON-serializable data to save
    """
    
    # Create a dictionary with time and data
    data_to_save = {
        "data": variable_data
    }
    # Write to JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data_to_save, json_file, indent=4)
    
    logger.info(f"Data saved to {file_path}")

def load_from_json(file_path: str)-> Dict[str, Any]:
    """
        Loads data from a JSON file
        
        filename (str): Path to the JSON file
        return: The loaded data or None if file doesn't exist
    """
    try:
        with open(file_path, 'r') as json_file:
            logger.info(f"Data loaded from {file_path}")
            return json.load(json_file)
    except FileNotFoundError:
        logger.error(f"File {file_path} not found")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {file_path}")
        return None
    
def delete_file(file_path):
    """ 
        Deletes file_path if it exists locally.
        
        file_path: directory path with name of file and extension
    """
    if os.path.exists(file_path):
        logger.info(f"{file_path} file has been deleted!")
        os.remove(file_path)
        
def check_file(file_path):
    """ 
        Check to see if file_path exists locally.
        
        file_path: directory path with name of file and extension
    """
    return os.path.exists(file_path)

def remove_items(all_items: List[Any], items_to_remove: List[Any])-> List[Any]:
    """ 
        Checks a list of items and deletes any that are within another list.
        
        all_items: a list of items
        items_to_remove: items to check and remove from 'all_items'
        
        return: 'all_items' minus any found in 'items_to_remove'
    """
    items_set = set(items_to_remove)
    return [item for item in all_items if item not in items_set]

def parse_library_purchase_history(dir_path: str)-> list[Dict]:
    if not os.path.isdir(dir_path):
        return
    
    html_files = [file for file in os.listdir(dir_path) if file.lower().endswith('.html')]
    if not html_files:
        return
    
    all_transactions = []
    for file in html_files:
        file_path = os.path.join(dir_path, file)
        
        if 'steam' in dir_path:
            transaction_data = parse_payment_history_steam(file_path)
        elif 'kinguin' in dir_path:
            print(True)
            transaction_data = parse_payment_history_kinguin(file_path)
        else:
            return
        all_transactions += transaction_data
        
    return all_transactions
            
def parse_payment_history_steam(filepath: str)-> List[Dict]:
    items = []
    if not filepath.endswith('.html'):
        return {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get individual items
        item = soup.find(class_='purchase_line_items')
        if not item:
            return []
        names = item.find_all(class_='purchase_detail_field')
        prices = item.find_all(class_='refund_value')
        
        for i in range(len(names)):
            price_text = prices[i].get_text()
            price = float(price_text.replace("$",''))
            price_cents = int(price * 100)
            items.append({"name": names[i].get_text(), "price":price_cents})
    except Exception as e:
            print(f"Error processing '{filepath}': {str(e)}")
    
    return items

def parse_payment_history_kinguin(filepath: str)-> List[Dict]:
    items = []
    if not filepath.endswith('.html'):
        return {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read() 
        soup = BeautifulSoup(html_content, 'html.parser')
        
        items = []
        # find all orders
        rows = soup.find_all(class_='sc-jwQYvw hlGyez')
        for row in rows:
            # don't process headers
            if row.find('th'):
                continue
            
            # each item bought
            cells = row.find_all('td', class_='sc-gFSQbh')
            name = cells[2].get_text()
            # extract game name only
            game_name = parse_game_name(name)
            
            # amount game was paid for in cents
            price = cells[5].get_text()
            price_in_cents = int(float(price.replace("$",'')) * 100)
            items.append({"name": game_name.strip(), "price":price_in_cents})
    except Exception as e:
            print(f"Error processing '{filepath}': {str(e)}")
    
    return items

def parse_game_name(name):
    game_name = ""
    if "PC" in name:
        game_name = name.split("PC")[0]
    elif "Steam" in name:
        game_name = name.split("Steam")[0]
    elif "EA" in name:
        game_name = name.split("EA")[0]
    elif "Origin" in name:
        game_name = name.split("Origin")[0]
        
    return game_name