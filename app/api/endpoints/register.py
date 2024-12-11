from fastapi import APIRouter, Query, Request, UploadFile, File, HTTPException, Form
from app.utils.face_recognition import encode_face, encode_face_bytes,correct_rotation_and_encode_face
from app.utils.face_recognition import correct_image_orientation
from app.utils.file_storage import load_metadata, save_encoding, save_metadata,save_image,get_unique_filename
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
    # if not valid_image(await image.read()):
    #     raise HTTPException(status_code=400, detail="This Format Is not supported")
    
    
    metadata = load_metadata()
   
    if employee_id in metadata:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    try:
        image_date=await image.read()
        correct_image_orientation(image_date)
        save_image(image_date, get_unique_filename(employee_id, image.filename.split('.')[-1]))
        #Image.open(get_unique_filename(employee_id, image.filename.split('.')[-1]))
        
        face_encoding = correct_rotation_and_encode_face(image_date)
        encoding_filename = save_encoding(employee_id, face_encoding)
        save_metadata(employee_id, name, encoding_filename)
        return {"employee_id": employee_id, "name": name}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# @router.post("/register-octet-stream")
# async def register_employee_octet_stream(
#      request:Request,
#     employee_id:str =    Query(...),
#     employee_name:str = Query(...)
# ):
#      return {
#          "employee_id": "not implemented",
#         "employee_name": "not implemented"
#      }
#      if not employee_id or not employee_name:
#         raise HTTPException(status_code=400, detail="Missing required fields")
     
#      data = await request.body()
#      if not data:
#         raise HTTPException(status_code=400, detail="Missing image")
#      if not valid_image(data):
#         raise HTTPException(status_code=400, detail="Invalid image format. Only PNG, JPG, and JPEG are allowed.")
     
#      metadata = load_metadata()

#      if employee_id in metadata:
#         raise HTTPException(status_code=400, detail="Employee ID already exists")
#      try:
#         face_encoding = correct_rotation_and_encode_face(data)
#         encoding_filename = save_encoding(employee_id, face_encoding)
#         save_metadata(employee_id, employee_name, encoding_filename)
#         return {"employee_id": employee_id, "name": employee_name}
#      except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))