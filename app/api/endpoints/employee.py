from fastapi import APIRouter, HTTPException
from app.utils.file_storage import load_metadata, delete_employee

router = APIRouter()

@router.delete("/employees/{employee_id}")
async def remove_employee(employee_id: str):
    metadata = load_metadata()
    if employee_id not in metadata:
        raise HTTPException(status_code=404, detail="Employee not found")
    delete_employee(employee_id)
    return {"msg": "Employee deleted successfully"}
@router.get("/employees")
async def list_employees():
    metadata = load_metadata()
    if not metadata:
        raise HTTPException(status_code=404, detail="No employees found")
    return [{"employee_id": employee_id, "name": details['name']} for employee_id, details in metadata.items()]
