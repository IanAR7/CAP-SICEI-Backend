from typing import List
from sqlalchemy.orm import Session
from infrastructure.db.database import get_db
from domain.repositories.test_student_repository import TestStudentRepository
from domain.entities.analytics import StudentFeatures
from infrastructure.db.models import StudentRiskTestDataset

class TestStudentRepositoryImpl(TestStudentRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all_test_students(self) -> List[StudentFeatures]:
        # Consultar todos los registros
        records = self.db.query(StudentRiskTestDataset).all()
        
        # Mapear a entidad de dominio
        students = []
        for r in records:
            student = StudentFeatures(
                internet_home=r.internet_home,
                has_laptop=r.has_laptop,
                is_female=r.is_female,
                age=r.age,
                works=r.works,
                num_people_home=r.num_people_home,
                prev_school_public=r.prev_school_public,
                finished_prev_school=r.finished_prev_school,
                repeated_subjects=r.repeated_subjects,
                work_hours=r.work_hours
            )
            students.append(student)
            
        return students
