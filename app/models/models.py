from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

ModelBase = declarative_base()


class Employee(ModelBase):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    free_days = Column(Integer())
    on_demand = Column(Integer(), default=4)


class Vacation(ModelBase):
    __tablename__ = "employee_vacation"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id", ondelete="CASCADE"))
    vacation_start = Column(DateTime())
    vacation_end = Column(DateTime())
    no_days = Column(Integer())
    on_demand = Column(Boolean())
