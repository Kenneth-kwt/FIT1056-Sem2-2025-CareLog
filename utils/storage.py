import json

def load_data(filepath):
    """
    Load JSON data from a file.
    If the file does not exist, return an empty list.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Data file not found. Starting with a clean state.")
    except json.JSONDecodeError:
        print("Data file is corrupted. Starting with a clean state.")
    return []

def save_data(filepath, data):
    """
    Save Python object (list/dict) as JSON into a file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)