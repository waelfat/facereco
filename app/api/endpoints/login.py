import io
import threading
import time
from typing import Any
import face_recognition
from fastapi import APIRouter, Query, Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.utils.face_recognition import correct_image_orientation, encode_face, compare_faces, encode_face_bytes,correct_rotation_and_encode_face,get_face_encoding_from_file
from app.utils.file_storage import load_metadata, load_encoding,save_image,get_globally_unique_filename,zip_images
from PIL import Image
from io import BytesIO
from pathlib import Path
import numpy as np
import logging
import concurrent.futures
def log_info(message):
    logging.info(message)
def log_error(message):
    logging.error(message)


router = APIRouter()
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_image_form_path_as_bytes(path:str) -> bytes:
    if not File_exists(path):
        raise HTTPException(status_code=400, detail="Image file not found")
    image=Image.open(path)
    img_byte_arr=io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    return img_byte_arr.getvalue()

def valid_image(bytes: bytes) -> bool:
    try:
        imget=Image.open(BytesIO(bytes))
        imget.verify()
        return True
    except:
        return False
def File_exists(path:str) -> bool:
    return Path(path).is_file()

    
def load_and_process_image(image_bytes:bytes):
    print(str(threading.current_thread().ident) +'\n')
    try:
        image = Image.open(BytesIO(image_bytes))
        endcoding=rotate_and_detect_faces(image)
        return endcoding
    # return correct_rotation_and_encode_face(image_bytes)
    except Exception as e:
        #log_error(f"Error processing image: {e}")
        return None
    

def rotate_and_detect_faces(image:Image.Image):
    for angle in [0,90,270,180]:
        print("angle: "+str(angle) +"\n")
        rotated_img = image.rotate(angle, expand=True)
        image_array = np.array(rotated_img)
        print("image_array")
        encodings = face_recognition.face_encodings(image_array)
        print("encodings fount")
        
        if encodings:
            return encodings[0]
    return None



# @router.post("/compare-faces/")
# async def compare_faces(image_path: str, file: UploadFile = File(...)):
#     start_time = time.time()
#     # Load and rotate the image from the path
#     if not File_exists(image_path):
#          raise HTTPException(status_code=400, detail="Image file not found")
#    # known_image = Image.open(image_path)
#     #uploaded_image = Image.open( file.file)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         known_encoding_future = executor.submit(rotate_and_detect_faces, Image.open(image_path))
#         uploaded_encoding_future = executor.submit(rotate_and_detect_faces, Image.open( file.file))
#         known_encoding = known_encoding_future.result()
#         uploaded_encoding = uploaded_encoding_future.result()
#     #known_encoding = rotate_and_detect_faces(known_image)
#     if  known_encoding is None:
#         raise HTTPException(status_code=400, detail="No face found in Database image.")
#     if  uploaded_encoding is None:
#         raise HTTPException(status_code=400, detail="No face found in uploaded image.")
#     # return {"match": False}
#     print("known_encoding")
#     # Read and rotate the uploaded image
    
#     print("uploaded_image_opened")
#     uploaded_encoding = rotate_and_detect_faces(uploaded_image)
#     if  uploaded_encoding is None:
#         raise HTTPException(status_code=400, detail="No face found in uploaded image.")
#     print("uploaded_encoding")

#     # Compare the faces
#     result = face_recognition.compare_faces([known_encoding], uploaded_encoding)
#     end_time = time.time()
#     print(f"Time taken: {end_time - start_time} seconds")
#     if not result[0]:
#         raise HTTPException(status_code=400, detail="Faces do not match.")
#     else:
#         return {"match": True}


@router.post("/compare-faces/")
async def compare_faces(image_path: str, file: UploadFile = File(...)):
    start_time = time.time()
    # Load and rotate the image from the path
    if not File_exists(image_path):
         raise HTTPException(status_code=400, detail="Image file not found")
    known_image = Image.open(image_path)
    known_encoding = rotate_and_detect_faces(known_image)
    if  known_encoding is None:
        raise HTTPException(status_code=400, detail="No face found in Database image.")
    # return {"match": False}
    print("known_encoding")
    # Read and rotate the uploaded image
    uploaded_image = Image.open( file.file)
    print("uploaded_image_opened")
    uploaded_encoding = rotate_and_detect_faces(uploaded_image)
    if  uploaded_encoding is None:
        raise HTTPException(status_code=400, detail="No face found in uploaded image.")
    print("uploaded_encoding")

    # Compare the faces
    result = face_recognition.compare_faces([known_encoding], uploaded_encoding)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    if not result[0]:
        raise HTTPException(status_code=400, detail="Faces do not match.")
    else:
        return {"match": True}

# @router.post("/matchfaces")
# async def match_faces(imagePath:str,image:UploadFile=File(...)):
#     if not imagePath:
#         raise HTTPException(status_code=400, detail="Missing required fields")
#     if not image:
#         raise HTTPException(status_code=400, detail="Missing image")
  
#     image_data = await image.read()
#     correct_image_orientation(Image.open(BytesIO(image_data)))
#     global_unique_filename = get_globally_unique_filename()
#     save_image(image_data, global_unique_filename)
#     #correct_image_orientation(Image.open(global_unique_filename))
#     image_face_encoding = correct_rotation_and_encode_face(image_data)
#     image_file = Image.open(imagePath)
#     image_bytes=load_image_form_path_as_bytes(imagePath)

    
#     print("imagefileloadded")
#     #image_file_encoding=get_face_encoding_from_file(imagePath)
#     print('image_file_encoding')
#     match = compare_faces(image_bytes, image_face_encoding)
#     return {"match": match}

 

        

@router.post("/login")
async def login(request: Request, image: UploadFile = File(...)):
      # Log request information including the client's IP address
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)
    client_host = request.client.host
    query_params = dict(request.query_params)
    log_info("Request received-----------")

    logging.info(f"Request method: {method}")
    logging.info(f"Request URL: {url}")
    logging.info(f"Request headers: {headers}")
    logging.info(f"Client host: {client_host}")
    logging.info(f"Query parameters: {query_params}")
    logging.info(f"Request loggedend -------------")

    if not image:
        log_error("Missing image")
        raise HTTPException(status_code=400, detail="Missing image")
    if not image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            log_error("Invalid image format. Only PNG, JPG, and JPEG are allowed.")
            raise HTTPException(status_code=400, detail="Invalid image format. Only PNG, JPG, and JPEG are allowed.")
    try:
        global_unique_filename = get_globally_unique_filename()
        image_data = await image.read()
        correct_image_orientation(Image.open(BytesIO(image_data)))
        save_image(image_data, global_unique_filename)
        face_encoding = correct_rotation_and_encode_face(image_data)
        #face_encoding = encode_face(global_unique_filename)
        metadata = load_metadata()
        for employee_id, details in metadata.items():
            known_face_encoding = load_encoding(details['encoding_filename'])
            if compare_faces(known_face_encoding, face_encoding):
                return {"employee_id": employee_id, "name": details['name']}
        log_error("Face not recognized")
        raise HTTPException(status_code=401, detail="Face not recognized")
    except ValueError as e:
        print(str(e) ,'wael')
        log_error(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    

    

@router.get("Test")
async def testEndpoint(test :str =Query(...)):
    if test != "in_1979":
        raise HTTPException(status_code=401, detail="Invalid password")

    
        # Current directory
    current_directory = '.'
    # Output zip file name
    output_zip_filename = 'images.zip'

    # Call the function
    zip_images(current_directory, output_zip_filename)
    return FileResponse(output_zip_filename, media_type='application/zip', filename=output_zip_filename)


# @router.post("/login-octet-stream")
# async def login_octet_stream(request:Request):
#     data = await request.body()
#     if not valid_image(data):

#         raise HTTPException(status_code=400, detail="Invalid image format. Only PNG, JPG, and JPEG are allowed.")
#     try:
       
#         face_encoding = encode_face_bytes(data)
#         metadata = load_metadata()
#         for employee_id, details in metadata.items():
#             known_face_encoding = load_encoding(details['encoding_filename'])
#             if compare_faces(known_face_encoding, face_encoding):
#                 return {"employee_id": employee_id, "name": details['name']}
#         raise HTTPException(status_code=401, detail="Face not recognized")
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))