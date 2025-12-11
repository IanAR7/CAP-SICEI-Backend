from domain.entities.grade import Grade, GradeToShowStudent, GradeToShowSubject
from infrastructure.db.models import GradeModel
from infrastructure.schemas.grades_schema import CreateGradeDTO, UpdateGradeDTO


def map_create_grade_dto_to_entity(grade_dto: CreateGradeDTO) -> Grade:
    """
    Maps a CreateGradeDTO to a Grade entity.

    Args:
        grade_dto (CreateGradeDTO): The DTO to map.

    Returns:
        Grade: The mapped Grade entity.
    """
    return Grade(
        id=None,
        student_id=grade_dto.student_id,
        subject_id=grade_dto.subject_id,
        value=grade_dto.value,
    )


def map_grade_entity_to_model(grade: Grade) -> GradeModel:
    """
    Maps a Grade entity to a GradeModel.

    Args:
        grade (Grade): The entity to map.

    Returns:
        GradeModel: The mapped model.
    """
    return GradeModel(
        id=grade.id,
        student_id=grade.student_id,
        subject_id=grade.subject_id,
        value=grade.value,
    )


def map_grade_model_to_entity(grade_model: GradeModel) -> Grade:
    """
    Maps a GradeModel to a Grade entity.

    Args:
        grade_model (GradeModel): The model to map.

    Returns:
        Grade: The mapped entity.
    """
    return Grade(
        id=grade_model.id,
        student_id=grade_model.student_id,
        subject_id=grade_model.subject_id,
        value=grade_model.value,
    )


def map_update_grade_dto_to_entity(grade_id: str, grade_dto: UpdateGradeDTO) -> Grade:
    """
    Maps an UpdateGradeDTO to a Grade entity.
    """
    return Grade(id=grade_id, student_id=None, subject_id=None, value=grade_dto.value)


def map_grade_model_to_grade_to_show_student_dto(
    grade_model: GradeModel,
) -> GradeToShowStudent:
    """
    Maps a GradeModel to a GradeToShow entity.

    Args:
        grade_model (GradeModel): The model to map.

    Returns:
        GradeToShow: The mapped entity.
    """
    return GradeToShowStudent(id=grade_model.id, subject=grade_model.subject.name, value=grade_model.value)


def map_grade_model_to_grade_to_show_subject_dto(
    grade_model: GradeModel,
) -> GradeToShowSubject:
    """
    Maps a GradeModel to a GradeToShow entity for subject display.

    Args:
        grade_model (GradeModel): The model to map.

    Returns:
        GradeToShow: The mapped entity.
    """
    return GradeToShowSubject(id=grade_model.id, student=grade_model.student.name, value=grade_model.value)
