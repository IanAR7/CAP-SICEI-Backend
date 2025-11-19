from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import uuid

Base = declarative_base()

class StudentModel(Base):
    __tablename__ = 'students'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    average = Column(Float, nullable=False, default=0.0)

class SubjectModel(Base):
    __tablename__ = 'subjects'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    credits = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

class GradeModel(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    subject_id = Column(String, ForeignKey("subjects.id"), nullable=False)
    value = Column(Float, nullable=False)

    student = relationship("StudentModel", backref="grades")
    subject = relationship("SubjectModel", backref="grades")