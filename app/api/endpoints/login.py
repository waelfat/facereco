from fastapi import APIRouter, Query, Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.utils.face_recognition import correct_image_orientation, encode_face, compare_faces, encode_face_bytes,correct_rotation_and_encode_face
from app.utils.file_storage import load_metadata, load_encoding,save_image,get_globally_unique_filename,zip_images
from PIL import Image
from io import BytesIO
import logging
def log_info(message):
    logging.info(message)
def log_error(message):
    logging.error(message)


router = APIRouter()
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def valid_image(bytes: bytes) -> bool:
    try:
        imget=Image.open(BytesIO(bytes))
        imget.verify()
        return True
    except:
        return False
    


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