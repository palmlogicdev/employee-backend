from pydantic import BaseModel

class employeeCreate(BaseModel):
    firstname: str
    lastname: str
    email: str
    salary: int
    role: str

class employeeUpdate(BaseModel):
    firstname: str
    lastname: str
    email: str
    salary: int
    role: str