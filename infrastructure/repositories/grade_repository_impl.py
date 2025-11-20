from typing import List, Optional

from sqlalchemy.orm import Session

from domain.entities.grade import Grade, GradeToShowStudent, GradeToShowSubject
from domain.repositories.grade_repository import GradeRepository
from infrastructure.db.models import GradeModel
from infrastructure.mappers.grade_mappers import (
    map_grade_entity_to_model,
    map_grade_model_to_entity,
    map_grade_model_to_grade_to_show_student_dto,
    map_grade_model_to_grade_to_show_subject_dto,
)
from infrastructure.utils.sort_fields import (
    ALLOWED_GRADES_SORT_FIELDS,
    ALLOWED_SORT_ORDERS,
)


class GradeRepositoryImpl(GradeRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, grade: Grade) -> Grade:
        grade_model = map_grade_entity_to_model(grade)
        self.db.add(grade_model)
        self.db.commit()
        self.db.refresh(grade_model)

        return Grade(
            id=grade_model.id,
            student_id=grade_model.student_id,
            subject_id=grade_model.subject_id,
            value=grade_model.value,
        )

    def get_by_id(self, grade_id: int) -> Grade | None:
        grade_model = self.db.query(GradeModel).filter(GradeModel.id == grade_id).first()

        if not grade_model:
            return None

        return map_grade_model_to_entity(grade_model)

    def get_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Grade]:
        query = self.db.query(GradeModel)

        if sort_field in ALLOWED_GRADES_SORT_FIELDS:
            if sort_order in ALLOWED_SORT_ORDERS and sort_order == "asc":
                query = query.order_by(getattr(GradeModel, sort_field).asc())
            elif sort_order in ALLOWED_SORT_ORDERS and sort_order == "desc":
                query = query.order_by(getattr(GradeModel, sort_field).desc())

        query = query.offset((page - 1) * page_size).limit(page_size)
        students_model = query.all()

        return [map_grade_model_to_entity(grade_model) for grade_model in students_model]

    def update(self, grade: Grade) -> Grade | None:
        grade_model = self.db.query(GradeModel).filter(GradeModel.id == grade.id).first()

        if not grade_model:
            return None

        if grade.value is not None:
            grade_model.value = grade.value

        self.db.commit()
        self.db.refresh(grade_model)

        return Grade(
            id=grade_model.id,
            student_id=grade_model.student_id,
            subject_id=grade_model.subject_id,
            value=grade_model.value,
        )

    def delete(self, grade_id: int) -> bool:
        grade_model = self.db.query(GradeModel).filter(GradeModel.id == grade_id).first()

        if not grade_model:
            return False

        self.db.delete(grade_model)
        self.db.commit()

        return True

    def exists(self, grade_id: int) -> bool:
        student_model = self.db.query(GradeModel).filter(GradeModel.id == grade_id).first()
        return student_model is not None

    def get_by_student_id(self, student_id: str) -> List[Grade] | None:
        grade_models = self.db.query(GradeModel).filter(GradeModel.student_id == student_id).all()

        if not grade_models:
            return None

        return [map_grade_model_to_entity(grade_model) for grade_model in grade_models]

    def get_by_subject_id(self, subject_id) -> List[Grade] | None:
        grade_models = self.db.query(GradeModel).filter(GradeModel.subject_id == subject_id).all()

        if not grade_models:
            return None

        return [map_grade_model_to_entity(grade_model) for grade_model in grade_models]

    def get_student_grades_to_show(self, student_id: str) -> List[GradeToShowStudent] | None:
        grade_models = self.db.query(GradeModel).filter(GradeModel.student_id == student_id).all()

        if not grade_models:
            return None

        return [map_grade_model_to_grade_to_show_student_dto(grade) for grade in grade_models]

    def get_subject_grades_to_show(self, subject_id: str) -> List[GradeToShowSubject] | None:
        grade_models = self.db.query(GradeModel).filter(GradeModel.subject_id == subject_id).all()

        if not grade_models:
            return None

        return [map_grade_model_to_grade_to_show_subject_dto(grade) for grade in grade_models]

    def is_regular_student(self, student_id: str) -> bool:
        grades = self.db.query(GradeModel.value).filter(GradeModel.student_id == student_id).all()

        if not grades:
            return False

        for (value,) in grades:
            if value < 70:
                return False

        return True
