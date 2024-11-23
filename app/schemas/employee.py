from pydantic import BaseModel, Field
from typing import Optional

class EmployeeBase(BaseModel):
    name: str = Field(..., example="John Doe")
    national_id:Optional[str] = Field(None, example="1234567890")
    company_employee_id: str = Field(..., example="EMP001")

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: str = Field(..., example="2c9e9e02-2c9e-2c9e-2c9e-2c9e2c9e2c9e")

class EmployeeOut(EmployeeBase):
    id: str
