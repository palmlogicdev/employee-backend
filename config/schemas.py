from pydantic import BaseModel

class employeeCreate(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    salary: int
    role: str