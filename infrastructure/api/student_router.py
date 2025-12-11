from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from application.use_cases.students.create_student import CreateStudentUseCase
from application.use_cases.students.delete_student import DeleteStudentUseCase
from application.use_cases.students.get_student import GetStudentUseCase
from application.use_cases.students.update_student import UpdateStudentUseCase
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.cannot_delete_resource_exception import (
    CannotDeleteResourceException,
)
from domain.exceptions.cannot_update_resource_exception import (
    CannotUpdateResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.utils.constants import UNEXPECTED_ERROR
from infrastructure.db.database import get_db
from infrastructure.mappers.student_mappers import (
    map_create_student_dto_to_entity,
    map_update_student_dto_to_entity,
)
from infrastructure.repositories.grade_repository_impl import GradeRepositoryImpl
from infrastructure.repositories.student_repository_impl import StudentRepositoryImpl
from infrastructure.repositories.subject_repository_impl import SubjectRepositoryImpl
from infrastructure.schemas.student_schema import CreateStudentDTO, StudentResponseDTO, UpdateStudentDTO

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=StudentResponseDTO)
async def create_student(student_data: CreateStudentDTO, db: Session = Depends(get_db)) -> StudentResponseDTO:
    try:
        repo = StudentRepositoryImpl(db)
        use_case = CreateStudentUseCase(repo)
        student = use_case.execute(map_create_student_dto_to_entity(student_data))
        return StudentResponseDTO.model_validate(student)
    except CannotCreateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get("/{student_id}", status_code=status.HTTP_200_OK, response_model=StudentResponseDTO)
async def get_student_by_id(student_id: str, db: Session = Depends(get_db)) -> StudentResponseDTO:
    try:
        repo = StudentRepositoryImpl(db)
        use_case = GetStudentUseCase(repo)
        student = use_case.execute_by_id(student_id)
        return StudentResponseDTO.model_validate(student)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=UNEXPECTED_ERROR + str(e)) from e


@router.get("/semester/{students_semester}", status_code=status.HTTP_200_OK, response_model=List[StudentResponseDTO])
async def get_students_by_semester(students_semester: int, db: Session = Depends(get_db)) -> List[StudentResponseDTO]:
    try:
        repo = StudentRepositoryImpl(db)
        use_case = GetStudentUseCase(repo)
        students = use_case.execute_by_semester(students_semester)
        return [StudentResponseDTO.model_validate(student) for student in students]
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[StudentResponseDTO])
async def get_all_students(
    db: Session = Depends(get_db),
    page_size: Annotated[int, Query(alias="pageSize")] = 25,
    current: Annotated[int, Query(alias="current")] = 1,
    sort_field: Optional[str] = Query(default=None, alias="sorters[0][field]"),
    sort_order: Optional[str] = Query(default=None, alias="sorters[0][order]"),
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


@router.put("/{student_id}", status_code=status.HTTP_200_OK, response_model=StudentResponseDTO)
async def update_student(student_id: str, student_data: UpdateStudentDTO, db: Session = Depends(get_db)) -> StudentResponseDTO:
    try:
        student_repo = StudentRepositoryImpl(db)
        subject_repo = SubjectRepositoryImpl(db)
        grade_repo = GradeRepositoryImpl(db)
        use_case = UpdateStudentUseCase(student_repo, subject_repo, grade_repo)
        updated_student = use_case.execute(map_update_student_dto_to_entity(student_id, student_data))
        return StudentResponseDTO.model_validate(updated_student)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except CannotUpdateResourceException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str, db: Session = Depends(get_db)):
    try:
        repo = StudentRepositoryImpl(db)
        use_case = DeleteStudentUseCase(repo)
        use_case.execute(student_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except CannotDeleteResourceException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e
