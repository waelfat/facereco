from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from app.utils.face_recognition import encode_face, compare_faces
from app.utils.file_storage import load_metadata, load_encoding
from PIL import Image
from io import BytesIO
router = APIRouter()
def valid_image(bytes: bytes) -> bool:
    try:
        imget=Image.open(BytesIO(bytes))
        imget.verify()
        return True
    except:
        return False

@router.post("/login")
async def login(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="Missing image")
    if not image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException(status_code=400, detail="Invalid image format. Only PNG, JPG, and JPEG are allowed.")
    try:
        face_encoding = encode_face(image)
        metadata = load_metadata()
        for employee_id, details in metadata.items():
            known_face_encoding = load_encoding(details['encoding_filename'])
            if compare_faces(known_face_encoding, face_encoding):
                return {"employee_id": employee_id, "name": details['name']}
        raise HTTPException(status_code=401, detail="Face not recognized")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.post("/login-octet-stream")
async def login_octet_stream(request:Request):
    data = await request.body()
    if not valid_image(data):
        raise HTTPException(status_code=400, detail="Invalid image format. Only PNG, JPG, and JPEG are allowed.")
    try:
        face_encoding = encode_face(data)
        metadata = load_metadata()
        for employee_id, details in metadata.items():
            known_face_encoding = load_encoding(details['encoding_filename'])
            if compare_faces(known_face_encoding, face_encoding):
                return {"employee_id": employee_id, "name": details['name']}
        raise HTTPException(status_code=401, detail="Face not recognized")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
   