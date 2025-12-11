from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from application.use_cases.grades.create_grade import CreateGradeUseCase
from application.use_cases.grades.delete_grade import DeleteGradeUseCase
from application.use_cases.grades.get_grade import GetGradeUseCase
from application.use_cases.grades.update_grade import UpdateGradeUseCase
from application.use_cases.students.get_student import GetStudentUseCase
from application.use_cases.subjects.get_subject import GetSubjectUseCase
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.cannot_delete_resource_exception import (
    CannotDeleteResourceException,
)
from domain.exceptions.cannot_update_resource_exception import (
    CannotUpdateResourceException,
)
from domain.exceptions.not_enough_arguments_exception import NotEnoughArgumentsException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.services.grade_service import GradeService
from domain.utils.constants import UNEXPECTED_ERROR
from domain.utils.exception_detail_wrapper import exception_detail_wrapper
from infrastructure.db.database import get_db
from infrastructure.mappers.grade_mappers import (
    map_create_grade_dto_to_entity,
    map_update_grade_dto_to_entity,
)
from infrastructure.repositories.grade_repository_impl import GradeRepositoryImpl
from infrastructure.repositories.student_repository_impl import StudentRepositoryImpl
from infrastructure.repositories.subject_repository_impl import SubjectRepositoryImpl
from infrastructure.schemas.grades_schema import (
    CreateGradeDTO,
    GradeResponseDTO,
    GradeToShowStudentResponseDTO,
    GradeToShowSubjectResponseDTO,
    UpdateGradeDTO,
)
from infrastructure.schemas.student_schema import StudentResponseDTO
from infrastructure.schemas.subject_schema import SubjectResponseDTO
from infrastructure.utils.constants import SORTERS_FIELD, SORTERS_ORDER

router = APIRouter(prefix="/grades", tags=["Grades"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GradeResponseDTO)
async def create_grade(grade_data: CreateGradeDTO, db: Session = Depends(get_db)) -> GradeResponseDTO:
    """
    Create a new grade.
    """
    try:
        repo = GradeRepositoryImpl(db)
        student_repo = StudentRepositoryImpl(db)
        subject_repo = SubjectRepositoryImpl(db)
        use_case = CreateGradeUseCase(repo, student_repo, subject_repo)
        grade = use_case.execute(map_create_grade_dto_to_entity(grade_data))
        return GradeResponseDTO.model_validate(grade)
    except NotEnoughArgumentsException as e:
        raise exception_detail_wrapper(
            status_code=status.HTTP_400_BAD_REQUEST,
            exception=e,
            error_type="NotEnoughArgumentsException",
        ) from e
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except CannotCreateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get("/students", status_code=status.HTTP_200_OK, response_model=List[StudentResponseDTO])
async def get_all_students(
    db: Session = Depends(get_db),
    page_size: Annotated[int, Query(alias="pageSize")] = 25,
    current: Annotated[int, Query(alias="current")] = 1,
    sort_field: Optional[str] = Query(default=None, alias=SORTERS_FIELD),
    sort_order: Optional[str] = Query(default=None, alias=SORTERS_ORDER),
) -> List[StudentResponseDTO]:
    try:
        repo = StudentRepositoryImpl(db)
        use_case = GetStudentUseCase(repo)
        students = use_case.execute_all(
            page_size=page_size,
            page=current,
            sort_field=sort_field,
            sort_order=sort_order,
        )
        return [StudentResponseDTO.model_validate(student) for student in students]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get("/subjects", status_code=status.HTTP_200_OK, response_model=List[SubjectResponseDTO])
async def get_all_subjects(
    db: Session = Depends(get_db),
    page_size: Annotated[int, Query(alias="pageSize")] = 25,
    current: Annotated[int, Query(alias="current")] = 1,
    sort_field: Optional[str] = Query(default=None, alias=SORTERS_FIELD),
    sort_order: Optional[str] = Query(default=None, alias=SORTERS_ORDER),
) -> List[SubjectResponseDTO]:
    try:
        repo = SubjectRepositoryImpl(db)
        use_case = GetSubjectUseCase(repo)
        subjects = use_case.execute_all(
            page_size=page_size,
            page=current,
            sort_field=sort_field,
            sort_order=sort_order,
        )
        return [SubjectResponseDTO.model_validate(subject) for subject in subjects]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get(
    "/students/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[GradeToShowStudentResponseDTO],
)
async def get_student_grades(
    student_id: str,
    db: Session = Depends(get_db),
) -> List[GradeToShowStudentResponseDTO]:
    repo = GradeRepositoryImpl(db)
    use_case = GetGradeUseCase(repo)
    students = use_case.execute_get_grades_by_student_id(student_id)
    return [GradeToShowStudentResponseDTO.model_validate(grade) for grade in students]


@router.get(
    "/subjects/{subject_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[GradeToShowSubjectResponseDTO],
)
async def get_subject_grades(
    subject_id: str,
    db: Session = Depends(get_db),
) -> List[GradeToShowSubjectResponseDTO]:
    repo = GradeRepositoryImpl(db)
    use_case = GetGradeUseCase(repo)
    subjects = use_case.execute_get_grades_by_subject_id(subject_id)
    return [GradeToShowSubjectResponseDTO.model_validate(grade) for grade in subjects]


@router.get("/{grade_id}", status_code=status.HTTP_200_OK, response_model=GradeResponseDTO)
async def get_grade_by_id(grade_id: int, db: Session = Depends(get_db)) -> GradeResponseDTO:
    """
    Get a grade by Id
    """
    try:
        repo = GradeRepositoryImpl(db)
        use_case = GetGradeUseCase(repo)
        grade = use_case.execute_by_id(grade_id)
        return GradeResponseDTO.model_validate(grade)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get(
    "/student/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[GradeResponseDTO],
)
async def get_grade_by_student_id(student_id: str, db: Session = Depends(get_db)) -> List[GradeResponseDTO]:
    try:
        repo = GradeRepositoryImpl(db)
        use_case = GetGradeUseCase(repo)
        grades = use_case.execute_by_student_id(student_id)
        return [GradeResponseDTO.model_validate(grade) for grade in grades]
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get(
    "/subject/{subject_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[GradeResponseDTO],
)
async def get_grade_by_subject_id(subject_id: str, db: Session = Depends(get_db)) -> List[GradeResponseDTO]:
    try:
        repo = GradeRepositoryImpl(db)
        use_case = GetGradeUseCase(repo)
        grades = use_case.execute_by_subject_id(subject_id)
        return [GradeResponseDTO.model_validate(grade) for grade in grades]
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[GradeResponseDTO])
async def get_all_grade(
    db: Session = Depends(get_db),
    page_size: Annotated[int, Query(alias="pageSize")] = 25,
    current: Annotated[int, Query(alias="current")] = 1,
    sort_field: Optional[str] = Query(default=None, alias=SORTERS_FIELD),
    sort_order: Optional[str] = Query(default=None, alias=SORTERS_ORDER),
) -> List[GradeResponseDTO]:
    try:
        repo = GradeRepositoryImpl(db)
        use_case = GetGradeUseCase(repo)
        grades = use_case.execute_all(
            page_size=page_size,
            page=current,
            sort_field=sort_field,
            sort_order=sort_order,
        )
        return [GradeResponseDTO.model_validate(grade) for grade in grades]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.put("/{grade_id}", status_code=status.HTTP_200_OK, response_model=GradeResponseDTO)
async def update_grade(grade_id: int, grade_data: UpdateGradeDTO, db: Session = Depends(get_db)) -> GradeResponseDTO:
    """
    Update a grade by Id
    """
    try:
        grade_repo = GradeRepositoryImpl(db)
        student_repo = StudentRepositoryImpl(db)
        grade_service = GradeService()
        use_case = UpdateGradeUseCase(grade_repo, student_repo, grade_service)
        grade = use_case.execute(map_update_grade_dto_to_entity(grade_id, grade_data))
        return GradeResponseDTO.model_validate(grade)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except CannotUpdateResourceException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(grade_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a grade by Id
    """
    try:
        repo = GradeRepositoryImpl(db)
        use_case = DeleteGradeUseCase(repo)
        use_case.execute(grade_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except CannotDeleteResourceException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e
