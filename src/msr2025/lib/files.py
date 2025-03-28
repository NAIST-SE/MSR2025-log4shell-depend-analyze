import json
import os
from pathlib import Path


def save_json(data, path: Path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
