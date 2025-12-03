from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import config.models as models
from config.schemas import employeeCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# root page
@app.get('/')
def root():
    return { 'detail': 'Hello, World' }

@app.post('/employee/', status_code=status.HTTP_201_CREATED)
def create_employee(employee: employeeCreate, db: Session = Depends(get_db)):

    db_employee = models.Employee(
        firstname = employee.firstname,
        lastname = employee.lastname,
        email = employee.email,
        salary = employee.salary,
        role = employee.role
    )

    db.add(db_employee)
    try:
        db.commit()
        db.refresh(db_employee)
    # rollback if employee.email is already in used
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in used")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return db_employee

@app.get('/employee/', status_code=status.HTTP_200_OK)
def get_all_employee(limit: int = 100, db: Session = Depends(get_db)):
    try:
        employees = db.query(models.Employee).limit(limit).all()
        if not employees:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No employees found")
        return employees
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Cannot get employees")
    
@app.get('/employee/{id}', status_code=status.HTTP_200_OK)
def get_employee_by_id(id: int, db: Session = Depends(get_db)):
    try:
        employee = db.query(models.Employee).filter(models.Employee.id == id).first()
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No employee found")
        return employee
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@app.delete('/employee/{id}', status_code=status.HTTP_200_OK)
def delete_employee_by_id(id: int, db: Session = Depends(get_db)):
    try:
        employee = db.query(models.Employee).filter(models.Employee.id == id).first()

        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No employee found")
        
        db.delete(employee)
        db.commit()

        return {'detail': f'Employee with id {id} has been deleted successfully'}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")