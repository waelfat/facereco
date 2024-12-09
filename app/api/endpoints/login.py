from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from app.utils.face_recognition import encode_face, compare_faces, encode_face_bytes
from app.utils.file_storage import load_metadata, load_encoding
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
        face_encoding = encode_face(image)
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
@router.post("/login-octet-stream")
async def login_octet_stream(request:Request):
    data = await request.body()
    if not valid_image(data):

        raise HTTPException(status_code=400, detail="Invalid image format. Only PNG, JPG, and JPEG are allowed.")
    try:
       
        face_encoding = encode_face_bytes(data)
        metadata = load_metadata()
        for employee_id, details in metadata.items():
            known_face_encoding = load_encoding(details['encoding_filename'])
            if compare_faces(known_face_encoding, face_encoding):
                return {"employee_id": employee_id, "name": details['name']}
        raise HTTPException(status_code=401, detail="Face not recognized")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
   