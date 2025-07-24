import json
import os

def load_settings():
    path = os.path.join(os.path.dirname(__file__), '..', 'settings.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)