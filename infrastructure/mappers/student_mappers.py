from domain.entities.student import Student
from infrastructure.db.models import StudentModel
from infrastructure.schemas.student_schema import CreateStudentDTO, UpdateStudentDTO


def map_create_student_dto_to_entity(student_dto: CreateStudentDTO) -> Student:
    """
    Maps a CreateStudentDTO to a Student entity.

    Args:
        student_dto (CreateStudentDTO): The DTO to map.

    Returns:
        Student: The mapped Student entity.
    """
    return Student(
        id=None,
        name=student_dto.name,
        lastname=student_dto.lastname,
        email=student_dto.email,
        semester=student_dto.semester,
    )


def map_student_entity_to_model(student: Student) -> StudentModel:
    """
    Maps a Student entity to a StudentModel.

    Args:
        student (Student): The entity to map.

    Returns:
        StudentModel: The mapped model.
    """
    return StudentModel(
        id=student.id,
        name=student.name,
        lastname=student.lastname,
        email=student.email,
        semester=student.semester,
    )


def map_student_model_to_entity(student_model: StudentModel) -> Student:
    """
    Maps a StudentModel to a Student entity.
    """
    return Student(
        id=student_model.id,
        name=student_model.name,
        lastname=student_model.lastname,
        email=student_model.email,
        semester=student_model.semester,
    )


def map_update_student_dto_to_entity(student_id: str, student_dto: UpdateStudentDTO) -> Student:
    """
    Maps an UpdateStudentDTO to a Student entity.

    Args:
        student_dto (UpdateStudentDTO): The DTO to map.

    Returns:
        Student: The mapped Student entity.
    """
    return Student(
        id=student_id,
        name=student_dto.name,
        lastname=student_dto.lastname,
        email=student_dto.email,
        semester=student_dto.semester,
    )
