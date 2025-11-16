from sqlalchemy.orm import Session
from typing import List, Optional

from domain.entities.professor import Professor
from domain.repositories.professor_repository import ProfessorRepository
from infrastructure.db.models import ProfessorModel
from infrastructure.mappers.professor_mappers import (
    map_professor_entity_to_model,
    map_professor_model_to_entity
)

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
    
    def get_by_user_id(self, user_id: str) -> Optional[Professor]:
        model = self.db.query(ProfessorModel).filter(
            ProfessorModel.user_id == user_id
        ).first()
        return map_professor_model_to_entity(model) if model else None
    
    def get_all(self) -> List[Professor]:
        models = self.db.query(ProfessorModel).all()
        return [map_professor_model_to_entity(m) for m in models]