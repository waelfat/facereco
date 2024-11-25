from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.face_recognition import encode_face, compare_faces

router = APIRouter()

@router.post("/match")
async def match_faces(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
):
    try:
        face_encoding1 = encode_face(image1)
        face_encoding2 = encode_face(image2)
        
        match = compare_faces(face_encoding1, face_encoding2)
        
        return {"match": match}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
