import json
from src import logger
import os
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