import json
import os
import numpy as np
from typing import Dict, Any

ENCODINGS_DIR = "encodings"
METADATA_FILE = "employee_metadata.json"

if not os.path.exists(ENCODINGS_DIR):
    os.makedirs(ENCODINGS_DIR)

metadata_cache = {}

def initialize_metadata() -> Dict[str, Any]:
    global metadata_cache
    if not os.path.exists(METADATA_FILE):
        metadata_cache = {}
        return metadata_cache
    try:
        with open(METADATA_FILE, "r") as f:
            metadata_cache = json.load(f)
    except (json.JSONDecodeError, EOFError):
        metadata_cache = {}
    return metadata_cache

def load_metadata() -> Dict[str, Any]:
    return metadata_cache

def save_metadata(employee_id: str, name: str, encoding_filename: str):
    global metadata_cache
    metadata_cache[employee_id] = {
        "name": name,
        "encoding_filename": encoding_filename
    }
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata_cache, f)

def save_encoding(employee_id: str, face_encoding: np.ndarray):
    filename = os.path.join(ENCODINGS_DIR, f"{employee_id}.npy")
    np.save(filename, face_encoding)
    return filename

def load_encoding(filename: str) -> np.ndarray:
    return np.load(filename)

def delete_employee(employee_id: str):
    global metadata_cache
    if employee_id in metadata_cache:
        encoding_filename = metadata_cache[employee_id]['encoding_filename']
        if os.path.exists(encoding_filename):
            os.remove(encoding_filename)
        del metadata_cache[employee_id]
        with open(METADATA_FILE, "w") as f:
            json.dump(metadata_cache, f)
