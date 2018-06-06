#!/usr/bin/python
# encoding: utf-8
'''
Created on 06.06.2018

@author: Andre Fiedler <andre@balticnetwork.de>
'''

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(Department, backref=backref('employees', uselist=True))
    
from sqlalchemy import create_engine
engine = create_engine('sqlite:////tmp/test.sqlite')
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

john = Employee(name='john')
it_department = Department(name='IT')
john.department = it_department

s = session()
s.add(john)
s.add(it_department)
s.commit()




