from sqlalchemy.orm import Session
from typing import List, Optional

from domain.entities.professor import Professor
from domain.repositories.professor_repository import ProfessorRepository
from infrastructure.db.models import ProfessorModel
from infrastructure.mappers.professor_mappers import (
    map_professor_entity_to_model,
    map_professor_model_to_entity
)

from infrastructure.utils.sort_fields import ALLOWED_PROFESSOR_SORT_FIELDS, ALLOWED_SORT_ORDERS


class ProfessorRepositoryImpl(ProfessorRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, professor: Professor) -> Professor:
        model = map_professor_entity_to_model(professor)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return map_professor_model_to_entity(model)

    def get_by_id(self, professor_id: str) -> Optional[Professor]:
        model = self.db.query(ProfessorModel).filter(
            ProfessorModel.id == professor_id
        ).first()
        return map_professor_model_to_entity(model) if model else None

    def get_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None
    ) -> List[Professor]:
        query = self.db.query(ProfessorModel)

        if sort_field in ALLOWED_PROFESSOR_SORT_FIELDS:
            if sort_order in ALLOWED_SORT_ORDERS and sort_order == "asc":
                query = query.order_by(getattr(ProfessorModel, sort_field).asc())
            elif sort_order in ALLOWED_SORT_ORDERS and sort_order == "desc":
                query = query.order_by(getattr(ProfessorModel, sort_field).desc())

        query = query.offset((page - 1) * page_size).limit(page_size)
        professors_model = query.all()

        return [map_professor_model_to_entity(professor_model) for professor_model in professors_model]

    def exists(self, professor_id: str) -> bool:
        return self.db.query(
            self.db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).exists()
        ).scalar()

    def update(self, professor: Professor) -> Optional[Professor]:
        professor_model = self.db.query(ProfessorModel).filter(ProfessorModel.id == professor.id).first()

        if not professor_model:
            return None

        if professor.first_name is not None:
            professor_model.first_name = professor.first_name
        if professor.last_name is not None:
            professor_model.last_name = professor.last_name
        if professor.email is not None:
            professor_model.email = professor.email
        if professor.phone is not None:
            professor_model.phone = professor.phone

        self.db.commit()
        self.db.refresh(professor_model)

        return map_professor_model_to_entity(professor_model)

    def delete(self, id: str) -> bool:
        professor_model = self.db.query(ProfessorModel).filter(ProfessorModel.id == id).first()

        if not professor_model:
            return False

        self.db.delete(professor_model)
        self.db.commit()
        return True