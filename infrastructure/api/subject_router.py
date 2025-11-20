from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from application.use_cases.subjects.create_subject import CreateSubjectUseCase
from application.use_cases.subjects.delete_subject import DeleteSubjectUseCase
from application.use_cases.subjects.get_subject import GetSubjectUseCase
from application.use_cases.subjects.update_subject import UpdateSubjectUseCase
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
from infrastructure.mappers.subject_mappers import (
    map_create_subject_dto_to_entity,
    map_update_subject_dto_to_entity,
)
from infrastructure.repositories.subject_repository_impl import SubjectRepositoryImpl
from infrastructure.schemas.subject_schema import (
    CreateSubjectDTO,
    SubjectResponseDTO,
    UpdateSubjectDTO,
)

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SubjectResponseDTO)
async def create_subject(subject_data: CreateSubjectDTO, db: Session = Depends(get_db)) -> SubjectResponseDTO:
    try:
        repo = SubjectRepositoryImpl(db)
        use_case = CreateSubjectUseCase(repo)
        subject = use_case.execute(map_create_subject_dto_to_entity(subject_data))
        return SubjectResponseDTO.model_validate(subject)
    except CannotCreateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get("/{subject_id}", status_code=status.HTTP_200_OK, response_model=SubjectResponseDTO)
async def get_subject_by_id(subject_id: str, db: Session = Depends(get_db)) -> SubjectResponseDTO:
    try:
        repo = SubjectRepositoryImpl(db)
        use_case = GetSubjectUseCase(repo)
        subject = use_case.execute_by_id(subject_id)
        return SubjectResponseDTO.model_validate(subject)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get(
    "/semester/{subjects_semester}",
    status_code=status.HTTP_200_OK,
    response_model=List[SubjectResponseDTO],
)
async def get_subjects_by_semester(subjects_semester: int, db: Session = Depends(get_db)) -> List[SubjectResponseDTO]:
    try:
        repo = SubjectRepositoryImpl(db)
        use_case = GetSubjectUseCase(repo)
        subjects = use_case.execute_by_semester(subjects_semester)
        return [SubjectResponseDTO.model_validate(subject) for subject in subjects]
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[SubjectResponseDTO])
async def get_all_subjects(
    db: Session = Depends(get_db),
    page_size: Annotated[int, Query(alias="pageSize")] = 25,
    current: Annotated[int, Query(alias="current")] = 1,
    sort_field: Optional[str] = Query(default=None, alias="sorters[0][field]"),
    sort_order: Optional[str] = Query(default=None, alias="sorters[0][order]"),
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


@router.put("/{subject_id}", status_code=status.HTTP_200_OK, response_model=SubjectResponseDTO)
async def update_subject(subject_id: str, subject_data: UpdateSubjectDTO, db: Session = Depends(get_db)) -> SubjectResponseDTO:
    try:
        repo = SubjectRepositoryImpl(db)
        use_case = UpdateSubjectUseCase(repo)
        updated_subject = use_case.execute(map_update_subject_dto_to_entity(subject_id, subject_data))
        return SubjectResponseDTO.model_validate(updated_subject)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except CannotUpdateResourceException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(subject_id: str, db: Session = Depends(get_db)):
    try:
        repo = SubjectRepositoryImpl(db)
        use_case = DeleteSubjectUseCase(repo)
        use_case.execute(subject_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except CannotDeleteResourceException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e),
        ) from e
