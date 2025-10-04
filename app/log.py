import json

class logManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/careLog.json"):
        self.data_path = data_path

        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        pass