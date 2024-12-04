from io import BytesIO
import face_recognition
import numpy as np

def encode_face(file) -> np.ndarray:
    image = face_recognition.load_image_file(file.file)
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