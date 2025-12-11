from fastapi import APIRouter, Depends, HTTPException, status, Query

from typing import Annotated, List, Optional

from sqlalchemy.orm import Session

from application.use_cases.professors.create_professor import CreateProfessorUseCase
from application.use_cases.professors.get_professor import GetProfessorUseCase
from application.use_cases.professors.update_professor import UpdateProfessorUseCase
from application.use_cases.professors.delete_professor import DeleteProfessorUseCase

from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.exceptions.cannot_update_resource_exception import CannotUpdateResourceException
from domain.exceptions.cannot_delete_resource_exception import CannotDeleteResourceException
from domain.utils.constants import UNEXPECTED_ERROR

from infrastructure.repositories.professor_repository_impl import ProfessorRepositoryImpl
from infrastructure.repositories.subject_repository_impl import SubjectRepositoryImpl
from infrastructure.schemas.professor_schema import CreateProfessorDTO, UpdateProfessorDTO, ProfessorResponseDTO
from infrastructure.mappers.professor_mappers import map_create_professor_dto_to_entity, map_update_professor_dto_to_entity
from infrastructure.db.database import get_db

router = APIRouter(prefix="/professors", tags=["Professors"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProfessorResponseDTO)
async def create_professor(
    professor_data: CreateProfessorDTO,
    db: Session = Depends(get_db)
) -> ProfessorResponseDTO:
    try:
        repo = ProfessorRepositoryImpl(db)
        use_case = CreateProfessorUseCase(repo)
        professor = use_case.execute(
            map_create_professor_dto_to_entity(professor_data)
        )
        return ProfessorResponseDTO.model_validate(professor)
    except CannotCreateException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.get("/{professor_id}", status_code=status.HTTP_200_OK, response_model=ProfessorResponseDTO)
async def get_professor_by_id(
    professor_id: str,
    db: Session = Depends(get_db)
) -> ProfessorResponseDTO:
    try:
        repo = ProfessorRepositoryImpl(db)
        use_case = GetProfessorUseCase(repo)
        professor = use_case.execute_by_id(professor_id)
        return ProfessorResponseDTO.model_validate(professor)
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ProfessorResponseDTO])
async def get_all_professors(
    db: Session = Depends(get_db),
    page_size: Annotated[int, Query(alias="pageSize")] = 25,
    current: Annotated[int, Query(alias="current")] = 1,
    sort_field: Optional[str] = Query(default=None, alias="sorters[0][field]"),
    sort_order: Optional[str] = Query(default=None, alias="sorters[0][order]")
) -> List[ProfessorResponseDTO]:
    try:
        repo = ProfessorRepositoryImpl(db)
        use_case = GetProfessorUseCase(repo)
        professors = use_case.execute_all(
            page_size=page_size,
            page=current,
            sort_field=sort_field,
            sort_order=sort_order
        )
        return [ProfessorResponseDTO.model_validate(professor) for professor in professors]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.put("/{professor_id}", status_code=status.HTTP_200_OK, response_model=ProfessorResponseDTO)
async def update_professor(
    professor_id: str,
    professor_data: UpdateProfessorDTO,
    db: Session = Depends(get_db)
) -> ProfessorResponseDTO:
    try:
        professor_repo = ProfessorRepositoryImpl(db)
        subject_repo = SubjectRepositoryImpl(db)
        use_case = UpdateProfessorUseCase(professor_repo, subject_repo)
        updated_professor = use_case.execute(
            map_update_professor_dto_to_entity(professor_id, professor_data)
        )
        return ProfessorResponseDTO.model_validate(updated_professor)
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except CannotUpdateResourceException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_professor(
    professor_id: str,
    db: Session = Depends(get_db)
):
    try:
        repo = ProfessorRepositoryImpl(db)
        use_case = DeleteProfessorUseCase(repo)
        use_case.execute(professor_id)
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except CannotDeleteResourceException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )
