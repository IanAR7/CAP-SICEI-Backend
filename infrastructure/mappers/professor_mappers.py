from domain.entities.professor import Professor
from infrastructure.db.models import ProfessorModel
from infrastructure.schemas.professor_schema import CreateProfessorDTO, UpdateProfessorDTO


def map_create_professor_dto_to_entity(professor_dto: CreateProfessorDTO) -> Professor:
    """
    Maps a CreateProfessorDTO to a Professor entity.
    """
    return Professor(id=None, first_name=professor_dto.first_name, last_name=professor_dto.last_name, email=professor_dto.email, phone=professor_dto.phone)


def map_professor_entity_to_model(professor: Professor) -> ProfessorModel:
    """
    Maps a Professor entity to a ProfessorModel (Database).
    """
    return ProfessorModel(
        id=professor.id,
        first_name=professor.first_name,
        last_name=professor.last_name,
        email=professor.email,
        phone=professor.phone,
    )


def map_professor_model_to_entity(professor_model: ProfessorModel) -> Professor:
    """
    Maps a ProfessorModel (Database) to a Professor entity.
    """
    return Professor(
        id=professor_model.id,
        first_name=professor_model.first_name,
        last_name=professor_model.last_name,
        email=professor_model.email,
        phone=professor_model.phone,
    )


def map_update_professor_dto_to_entity(professor_id: str, professor_dto: UpdateProfessorDTO) -> Professor:
    """
    Maps an UpdateProfessorDTO to a Professor entity for updating purposes.
    Note: We set fields to the DTO value. If the DTO value is None, the repository logic
    should handle avoiding overwriting with None, OR the entity logic handles the merge.
    Usually, this entity is used to carry the new data.
    """
    return Professor(
        id=professor_id,
        first_name=professor_dto.first_name if professor_dto.first_name else "",
        last_name=professor_dto.last_name if professor_dto.last_name else "",
        email=professor_dto.email if professor_dto.email else "",
        phone=professor_dto.phone,
    )
