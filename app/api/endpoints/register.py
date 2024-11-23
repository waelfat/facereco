from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.utils.face_recognition import encode_face
from app.utils.file_storage import load_metadata, save_encoding, save_metadata

router = APIRouter()

@router.post("/register")
async def register_employee(
    employee_id: str = Form(...),
    name: str = Form(...),
    image: UploadFile = File(...),
):
    if not employee_id or not name or not image:
        raise HTTPException(status_code=400, detail="Missing required fields")
    if not image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException(status_code=400, detail="Invalid image format. Only PNG, JPG, and JPEG are allowed.")
    
    metadata = load_metadata()
   
    if employee_id in metadata:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    try:
        face_encoding = encode_face(image)
        encoding_filename = save_encoding(employee_id, face_encoding)
        save_metadata(employee_id, name, encoding_filename)
        return {"employee_id": employee_id, "name": name}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
