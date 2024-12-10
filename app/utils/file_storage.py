from io import BytesIO
import json
import os
import zipfile
import numpy as np
from typing import Dict, Any
from PIL import Image
import uuid
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

# def save_image(image: bytes):

#     filename =  'waelname' + ".jpg"
#     with open(filename, "wb") as f:
#         f.write(image)

def create_unique_file_name ():
    import uuid
    return str(uuid.uuid4())



def save_image(bytes: bytes, filename: str) -> bool:
    try:
        imget=Image.open(BytesIO(bytes))
        imget.save(filename, format=imget.format)
        return True
    except:
        return False
    
def get_unique_filename(employee_id: str, extension: str) -> str:
    return f"{employee_id}.{extension}"
def get_globally_unique_filename():
    return uuid.uuid4().hex + ".jpg"


def zip_images(directory, output_filename):
    # Create a ZipFile object
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        # Iterate over all files in the directory
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                # Check if the file is an image
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    # Create a complete filepath of the file
                    file_path = os.path.join(foldername, filename)
                    # Add file to the zip
                    zipf.write(file_path, arcname=filename)
    print(f"All images have been zipped into {output_filename}")


