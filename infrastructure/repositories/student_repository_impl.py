from sqlalchemy.orm import Session

from typing import List, Optional

from domain.entities.student import Student
from domain.repositories.student_repository import StudentRepository

from infrastructure.db.models import StudentModel
from infrastructure.utils.sort_fields import ALLOWED_STUDENT_SORT_FIELDS, ALLOWED_SORT_ORDERS
from infrastructure.mappers.student_mappers import map_student_entity_to_model, map_student_model_to_entity

class StudentRepositoryImpl(StudentRepository):
    """Implementation of the StudentRepository interface using SQLAlchemy."""
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, student: Student) -> Student:
        student_model = map_student_entity_to_model(student)
        self.db.add(student_model)
        self.db.commit()
        self.db.refresh(student_model)
        
        return Student(
            id=student_model.id,
            name=student_model.name,
            lastname=student_model.lastname,
            email=student_model.email,
            semester=student_model.semester
        )
    
    def get_by_id(self, student_id: str) -> Student | None:
        student_model = self.db.query(StudentModel).filter(StudentModel.id == student_id).first()

        if not student_model:
            return None
        
        return map_student_model_to_entity(student_model)

    def get_by_semester(self, students_semester: int) -> List[Student]:
        students_model = self.db.query(StudentModel).filter(StudentModel.semester == students_semester).all()
        return [map_student_model_to_entity(student_model) for student_model in students_model]

    def get_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None
    ) -> List[Student]:
        query = self.db.query(StudentModel)

        if sort_field in ALLOWED_STUDENT_SORT_FIELDS:
            if sort_order in ALLOWED_SORT_ORDERS and sort_order == "asc":
                query = query.order_by(getattr(StudentModel, sort_field).asc())
            elif sort_order in ALLOWED_SORT_ORDERS and sort_order == "desc":
                query = query.order_by(getattr(StudentModel, sort_field).desc())
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        students_model = query.all()

        return [map_student_model_to_entity(student_model) for student_model in students_model]

    def update(self, student: Student) -> Student | None:
        student_model = self.db.query(StudentModel).filter(StudentModel.id == student.id).first()
        
        if not student_model:
            return None
        
        if student.name is not None:
            student_model.name = student.name
        if student.lastname is not None:
            student_model.lastname = student.lastname
        if student.email is not None:
            student_model.email = student.email
        if student.semester is not None:
            student_model.semester = student.semester
        if student.average is not None:
            student_model.average = student.average

        self.db.commit()
        self.db.refresh(student_model)

        return Student(
            id=student_model.id,
            name=student_model.name,
            lastname=student_model.lastname,
            email=student_model.email,
            semester=student_model.semester,
            average=student_model.average,
        )

    def delete(self, student_id: str) -> bool:
        student_model = self.db.query(StudentModel).filter(StudentModel.id == student_id).first()

        if not student_model:
            return False
        
        self.db.delete(student_model)
        self.db.commit()
        
        return True
    
    def exists(self, student_id: str) -> bool:
        student_obtained = self.db.query(StudentModel).filter(StudentModel.id == student_id).first()
        return student_obtained is not None
    
    def get_average_by_student_id(self, student_id: str) -> float | None:
        """To get the average grade of a student by their ID. Implementation"""
        return (
            self.db.query(StudentModel.average)
            .filter(StudentModel.id == student_id)
            .scalar()
        )