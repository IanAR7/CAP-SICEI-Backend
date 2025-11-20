from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from application.use_cases.reports.get_report import GetReportUseCase
from infrastructure.db.database import get_db
from infrastructure.repositories.grade_repository_impl import GradeRepositoryImpl
from infrastructure.repositories.student_repository_impl import StudentRepositoryImpl
from infrastructure.schemas.report_schema import (
    ReportStudentsResponseDTO,
    ReportSubjectsResponseDTO,
    StudentsDashboardResponseDTO,
)
from infrastructure.utils.constants import SORTERS_FIELD, SORTERS_ORDER

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get(
    "/students/{student_id}/grades",
    status_code=status.HTTP_200_OK,
    response_model=ReportStudentsResponseDTO,
)
async def get_student_subjects_grades(student_id: str, db: Session = Depends(get_db)) -> ReportStudentsResponseDTO:
    """
    Get grades with average for a specific student by their ID.
    """
    try:
        student_repo = StudentRepositoryImpl(db)
        grade_repo = GradeRepositoryImpl(db)
        use_case = GetReportUseCase(student_repository=student_repo, grade_repository=grade_repo)
        grades, average = use_case.execute_by_student_id(student_id)
        return ReportStudentsResponseDTO(subjects=grades, average=average)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing use case: {str(e)}",
        ) from e


@router.get(
    "/subjects/{subject_id}/grades",
    status_code=status.HTTP_200_OK,
    response_model=ReportSubjectsResponseDTO,
)
async def get_subject_students_grades(subject_id: str, db: Session = Depends(get_db)) -> ReportSubjectsResponseDTO:
    """
    Get students with grades for a specific subject by its ID.
    """
    try:
        student_repo = StudentRepositoryImpl(db)
        grade_repo = GradeRepositoryImpl(db)
        use_case = GetReportUseCase(student_repository=student_repo, grade_repository=grade_repo)
        students, average = use_case.execute_by_subject_id(subject_id)
        return ReportSubjectsResponseDTO(students=students, average=average)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing use case: {str(e)}",
        ) from e


@router.get(
    "/students",
    status_code=status.HTTP_200_OK,
    response_model=List[StudentsDashboardResponseDTO],
)
async def get_all_students_for_dashboard(
    db: Session = Depends(get_db),
    page_size: Annotated[int, Query(alias="pageSize")] = 25,
    current: Annotated[int, Query(alias="current")] = 1,
    sort_field: Optional[str] = Query(default=None, alias=SORTERS_FIELD),
    sort_order: Optional[str] = Query(default=None, alias=SORTERS_ORDER),
) -> List[StudentsDashboardResponseDTO]:
    """
    Get all the students for the students dashboard
    """

    try:
        student_repo = StudentRepositoryImpl(db)
        grade_repo = GradeRepositoryImpl(db)
        use_case = GetReportUseCase(student_repository=student_repo, grade_repository=grade_repo)
        students = use_case.execute_all_students_dashboard(
            page_size=page_size,
            page=current,
            sort_field=sort_field,
            sort_order=sort_order,
        )
        return [StudentsDashboardResponseDTO.model_validate(student) for student in students]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing use case: {str(e)}",
        ) from e
