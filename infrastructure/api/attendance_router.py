from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from application.use_cases.attendances.create_attendance import CreateAttendanceUseCase
from application.use_cases.attendances.get_attendance import GetAttendanceUseCase
from application.use_cases.attendances.update_attendance import UpdateAttendanceUseCase
from application.use_cases.attendances.delete_attendance import DeleteAttendanceUseCase
from application.use_cases.attendances.get_attendance_analytics import GetAttendanceAnalyticsUseCase

from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.exceptions.cannot_update_resource_exception import CannotUpdateResourceException
from domain.exceptions.cannot_delete_resource_exception import CannotDeleteResourceException
from domain.utils.constants import UNEXPECTED_ERROR

from infrastructure.db.database import get_db
from infrastructure.repositories.attendance_repository_impl import AttendanceRepositoryImpl
from infrastructure.repositories.student_repository_impl import StudentRepositoryImpl
from infrastructure.repositories.subject_repository_impl import SubjectRepositoryImpl
from infrastructure.repositories.professor_repository_impl import ProfessorRepositoryImpl
from infrastructure.schemas.attendance_schema import (CreateAttendanceDTO, UpdateAttendanceDTO, AttendanceResponseDTO, AttendanceAnalyticsDTO)
from infrastructure.mappers.attendance_mappers import (map_create_attendance_dto_to_entity, map_update_attendance_dto_to_entity)

router = APIRouter(prefix="/attendances", tags=["Attendances"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AttendanceResponseDTO)
async def create_attendance(
    attendance_data: CreateAttendanceDTO,
    db: Session = Depends(get_db)
) -> AttendanceResponseDTO:
    """
    Create attendance record.
    """
    try:
        attendance_repo = AttendanceRepositoryImpl(db)
        student_repo = StudentRepositoryImpl(db)
        subject_repo = SubjectRepositoryImpl(db)
        professor_repo = ProfessorRepositoryImpl(db)
        
        use_case = CreateAttendanceUseCase(
            attendance_repo,
            student_repo,
            subject_repo,
            professor_repo
        )
        
        attendance = use_case.execute(
            map_create_attendance_dto_to_entity(attendance_data)
        )
        return AttendanceResponseDTO.model_validate(attendance)
    
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
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

@router.get("/{attendance_id}", status_code=status.HTTP_200_OK, response_model=AttendanceResponseDTO)
async def get_attendance_by_id(
    attendance_id: str,
    db: Session = Depends(get_db)
) -> AttendanceResponseDTO:
    """
    Get assistance by ID.
    """
    try:
        repo = AttendanceRepositoryImpl(db)
        use_case = GetAttendanceUseCase(repo)
        attendance = use_case.execute_by_id(attendance_id)
        return AttendanceResponseDTO.model_validate(attendance)
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

@router.get("/student/{student_id}", status_code=status.HTTP_200_OK, response_model=List[AttendanceResponseDTO])
async def get_attendances_by_student(
    student_id: str,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
) -> List[AttendanceResponseDTO]:
    """
    Get attendances from a student.
    """
    try:
        repo = AttendanceRepositoryImpl(db)
        use_case = GetAttendanceUseCase(repo)
        attendances = use_case.execute_by_student(student_id, start_date, end_date)
        return [AttendanceResponseDTO.model_validate(a) for a in attendances]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.get("/subject/{subject_id}", status_code=status.HTTP_200_OK, response_model=List[AttendanceResponseDTO])
async def get_attendances_by_subject(
    subject_id: str,
    date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
) -> List[AttendanceResponseDTO]:
    """
    Get attendances with a subject.
    """
    try:
        repo = AttendanceRepositoryImpl(db)
        use_case = GetAttendanceUseCase(repo)
        attendances = use_case.execute_by_subject(subject_id, date)
        return [AttendanceResponseDTO.model_validate(a) for a in attendances]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.get("/analytics/student/{student_id}", status_code=status.HTTP_200_OK, response_model=AttendanceAnalyticsDTO)
async def get_student_attendance_analytics(
    student_id: str,
    subject_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
) -> AttendanceAnalyticsDTO:
    """
    Get attendance statistics for ML.
    """
    try:
        repo = AttendanceRepositoryImpl(db)
        use_case = GetAttendanceAnalyticsUseCase(repo)
        stats = use_case.execute(student_id, subject_id)
        return AttendanceAnalyticsDTO(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.put("/{attendance_id}", status_code=status.HTTP_200_OK, response_model=AttendanceResponseDTO)
async def update_attendance(
    attendance_id: str,
    attendance_data: UpdateAttendanceDTO,
    db: Session = Depends(get_db)
) -> AttendanceResponseDTO:
    """
    Update attendance.
    """
    try:
        repo = AttendanceRepositoryImpl(db)
        use_case = UpdateAttendanceUseCase(repo)
        attendance = use_case.execute(
            map_update_attendance_dto_to_entity(attendance_id, attendance_data)
        )
        return AttendanceResponseDTO.model_validate(attendance)
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

@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(
    attendance_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete attendance.
    """
    try:
        repo = AttendanceRepositoryImpl(db)
        use_case = DeleteAttendanceUseCase(repo)
        use_case.execute(attendance_id)
    except CannotDeleteResourceException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )