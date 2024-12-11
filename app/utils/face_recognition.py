from io import BytesIO
import face_recognition
from PIL import Image, ExifTags
import logging

import numpy as np
page_processing_logger =logging.getLogger("page_processing")
page_processing_logger.setLevel(logging.DEBUG)
def log_error(message: str):
    page_processing_logger.error(message)

def log_info(message: str):
    page_processing_logger.info(message)

file_handler=logging.FileHandler("page_processing.log")
file_handler.setLevel(logging.INFO)
page_processing_logger.addHandler(file_handler)

file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))



def correct_rotation_and_encode_face(image_bytes: bytes) -> np.ndarray:
    angles=[0,90,270,180]
    image = Image.open(BytesIO(image_bytes))
    
    for angle in angles:
        rotated_image = image.rotate(angle, expand=True)
        with BytesIO() as buffer:
            rotated_image.save(buffer, format='JPEG')
            rotated_image_bytes = buffer.getvalue()
           
            face_encodings = face_recognition.face_encodings(face_recognition.load_image_file(BytesIO(rotated_image_bytes)))
            if len(face_encodings) > 0:
                log_info(f"Face found after rotation of {angle} degrees")
                return np.array(face_encodings[0], dtype=np.float64)
    
    log_error("No faces found after rotation")
    raise ValueError("No faces found")
        


        

def encode_face(file) -> np.ndarray:
    image = face_recognition.load_image_file(file)
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) == 0:
        raise ValueError("No faces found")
    return np.array(face_encodings[0], dtype=np.float64)


def compare_faces(known_face_encoding: np.ndarray, face_encoding: np.ndarray) -> bool:
    return face_recognition.compare_faces([known_face_encoding], face_encoding)[0]




def encode_face_bytes(file:bytes) -> np.ndarray:
    image = face_recognition.load_image_file(BytesIO(file))
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) == 0:
        raise ValueError("No faces found")
    return np.array(face_encodings[0], dtype=np.float64)




def correct_image_orientation(image: Image.Image) :
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                page_processing_logger.log(logging.INFO, f"Orientation tag found: {orientation}")
                
                break
        exif = image._getexif()
        
        if exif is not None:
            orientation = exif.get(orientation, None)
            page_processing_logger.log(logging.INFO, f"Orientation value: {orientation}")
            
            if orientation == 3:
                
                image = image.rotate(180, expand=True)
                page_processing_logger.log(logging.INFO, "Rotated 180 degrees")
                
            elif orientation == 6:
                image = image.rotate(-90, expand=True)
                page_processing_logger.log(logging.INFO, "Rotated -90 degrees")

            elif orientation == 8:
                image = image.rotate(90, expand=True)
                page_processing_logger.log(logging.INFO, "Rotated 90 degrees")
    except (AttributeError, KeyError, IndexError):
        # Cases: image doesn't have getexif
        page_processing_logger.log(logging.INFO, "No EXIF data found")
        pass

    
