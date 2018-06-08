#!/usr/bin/python
# encoding: utf-8
'''
Created on 06.06.2018

@author: Andre Fiedler <andre@balticnetwork.de>
'''

from sqlalchemy import Column, String, Integer, ForeignKey, select
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, ResourceClosedError
from numpy.lib import financial


Base = declarative_base()

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    employees = relationship('Employee', secondary='department_employee')
    
class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    departments = relationship('Department', secondary='department_employee')
    
class DepartmentEmployee(Base):
    __tablename__ = 'department_employee'
    department_id = Column(Integer, ForeignKey('department.id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    
from sqlalchemy import create_engine
engine = create_engine('sqlite:////tmp/test.sqlite')
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

s = Session() #: :type a: sqlalchemy.orm.session.Session


try:
    
    john = Employee(name='john')
    s.add(john)
    it_department = Department(name='IT')
    it_department.employees.append(john)
    s.add(it_department)
    s.commit()
    
except IntegrityError, e:
    print "Error: %s" % repr(e)
    s.rollback()

try:
    marry = Employee(name='marry')
    financial_department = Department(name='financial')
    financial_department.employees.append(marry)
    s.add(marry)
    s.add(financial_department)
    s.commit()
except IntegrityError, e:
    print "Error: %s" % repr(e)
    s.rollback()
    
try:
    boss = Employee(name='boss')
    financial_department = s.query(Department).filter(Department.name=='IT').one()
    it_department = s.query(Department).filter(Department.name=='financial').one()
    boss.departments = [financial_department,it_department]
    s.add(boss)
        
    
    s.commit()
except IntegrityError, e:
    print "Add boss Error: %s" % repr(e)
    s.rollback()


try:
    #find_it = select([Department.id]).where(Department.name == 'IT')
    #rs = s.execute(find_it)
    #print rs.fetchone()
    john = s.query(Employee).filter(Employee.name == 'john').one()
    print repr(john)
    print len(john.departments)
    print john.departments[0].name
except ResourceClosedError, e:
    print "Error %s" % repr(e)
    s.rollback()


