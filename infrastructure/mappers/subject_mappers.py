from domain.entities.subject import Subject

from infrastructure.schemas.subject_schema import CreateSubjectDTO, UpdateSubjectDTO
from infrastructure.db.models import SubjectModel

def map_create_subject_dto_to_entity(subject_dto: CreateSubjectDTO) -> Subject:
    """
    Maps a CreateSubjectDTO to a Subject entity.

    Args:
        subject_dto (CreateSubjectDTO): The DTO to map.

    Returns:
        Subject: The mapped Subject entity.
    """
    return Subject(
        id=None,
        name=subject_dto.name,
        description=subject_dto.description,
        credits=subject_dto.credits,
        semester=subject_dto.semester,
        professor_id=subject_dto.professor_id
    )

def map_subject_entity_to_model(subject: Subject) -> SubjectModel:
    """
    Maps a Subject entity to a SubjectModel.

    Args:
        subject (Subject): The entity to map.

    Returns:
        SubjectModel: The mapped model.
    """
    return SubjectModel(
        id=subject.id,
        name=subject.name,
        description=subject.description,
        credits=subject.credits,
        semester=subject.semester,
        professor_id=subject.professor_id
    )

def map_subject_model_to_entity(subject_model: SubjectModel) -> Subject:
    """
    Maps a SubjectModel to a Subject entity.
    """
    return Subject(
        id=subject_model.id,
        name=subject_model.name,
        description=subject_model.description,
        credits=subject_model.credits,
        semester=subject_model.semester,
        professor_id=subject_model.professor_id
    )

def map_update_subject_dto_to_entity(subject_id: str, subject_dto: UpdateSubjectDTO) -> Subject:
    """
    Maps an UpdateSubjectDTO to a Subject entity.

    Args:
        subject_dto (UpdateSubjectDTO): The DTO to map.

    Returns:
        Subject: The mapped Subject entity.
    """
    return Subject(
        id=subject_id,
        name=subject_dto.name,
        description=subject_dto.description,
        credits=subject_dto.credits,
        semester=subject_dto.semester,
        professor_id=None  # Assuming professor_id is not updated via UpdateSubjectDTO
    )