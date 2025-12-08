from sqlalchemy import Column, Integer, String
from config.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    salary = Column(Integer, nullable=False)
    role = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)