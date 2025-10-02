from typing import Any, Dict

import json
from datetime import datetime


def load_rules(file_path: str) -> Any:
    """Load JSON data from a file."""
    import json
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path: str) -> None:
    """Save data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def _convert_timestamp(timestamp):
        """
        Converts Gmail internalDate (milliseconds since epoch as string) to PostgreSQL TIMESTAMP.
        """
        if not timestamp:
            return datetime.now()
        try:
            # Gmail internalDate is in milliseconds
            ts = int(timestamp) / 1000
            return datetime.fromtimestamp(ts)
        except Exception as e:
            return datetime.now()