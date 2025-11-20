from unittest.mock import Mock

import pytest

from application.use_cases.reports.get_report import GetReportUseCase
from domain.entities.grade import GradeToShowStudent, GradeToShowSubject
from domain.entities.student import Student, StudentReportDashboard
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException


class TestGetReportUseCase:
    @pytest.fixture
    def mock_grade_repository(self):
        return Mock()

    @pytest.fixture
    def mock_student_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_grade_repository, mock_student_repository):
        return GetReportUseCase(
            grade_repository=mock_grade_repository,
            student_repository=mock_student_repository,
        )

    # ========== Tests for execute_by_student_id ==========

    def test_execute_by_student_id_success(self, use_case, mock_grade_repository, mock_student_repository):
        student_id = "S001"
        expected_grades = [
            GradeToShowStudent(id=1, subject="Matemáticas", value=85.0),
            GradeToShowStudent(id=2, subject="Física", value=90.0),
        ]
        expected_average = 87.5

        mock_grade_repository.get_student_grades_to_show.return_value = expected_grades
        mock_student_repository.get_average_by_student_id.return_value = expected_average

        grades, average = use_case.execute_by_student_id(student_id)

        assert grades == expected_grades
        assert average == expected_average
        mock_grade_repository.get_student_grades_to_show.assert_called_once_with(student_id)
        mock_student_repository.get_average_by_student_id.assert_called_once_with(student_id)

    def test_execute_by_student_id_no_grades(self, use_case, mock_grade_repository, mock_student_repository):
        student_id = "S999"
        mock_grade_repository.get_student_grades_to_show.return_value = None
        mock_student_repository.get_average_by_student_id.return_value = 85.0

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_student_id(student_id)

        assert f"Cannot fount data for student with ID '{student_id}'" in str(exc_info.value)

    def test_execute_by_student_id_no_average(self, use_case, mock_grade_repository, mock_student_repository):
        student_id = "S001"
        expected_grades = [GradeToShowStudent(id=1, subject="Matemáticas", value=85.0)]

        mock_grade_repository.get_student_grades_to_show.return_value = expected_grades
        mock_student_repository.get_average_by_student_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_student_id(student_id)

        assert f"Cannot fount data for student with ID '{student_id}'" in str(exc_info.value)

    def test_execute_by_student_id_empty_grades_list(self, use_case, mock_grade_repository, mock_student_repository):
        student_id = "S001"
        mock_grade_repository.get_student_grades_to_show.return_value = []
        mock_student_repository.get_average_by_student_id.return_value = 0.0

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_student_id(student_id)

        assert f"Cannot fount data for student with ID '{student_id}'" in str(exc_info.value)

    # ========== Tests for execute_by_subject_id ==========

    def test_execute_by_subject_id_success(self, use_case, mock_grade_repository):
        subject_id = "SUB001"
        expected_grades = [
            GradeToShowSubject(id=1, student="Juan Pérez", value=80.0),
            GradeToShowSubject(id=2, student="María García", value=90.0),
            GradeToShowSubject(id=3, student="Pedro López", value=85.0),
        ]
        expected_average = 85.0

        mock_grade_repository.get_subject_grades_to_show.return_value = expected_grades

        grades, average = use_case.execute_by_subject_id(subject_id)

        assert grades == expected_grades
        assert average == expected_average
        mock_grade_repository.get_subject_grades_to_show.assert_called_once_with(subject_id)

    def test_execute_by_subject_id_not_found(self, use_case, mock_grade_repository):
        subject_id = "SUB999"
        mock_grade_repository.get_subject_grades_to_show.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_subject_id(subject_id)

        assert f"Cannot found data for subject with ID '{subject_id}'" in str(exc_info.value)

    def test_execute_by_subject_id_empty_list(self, use_case, mock_grade_repository):
        subject_id = "SUB001"
        mock_grade_repository.get_subject_grades_to_show.return_value = []

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_subject_id(subject_id)

        assert f"Cannot found data for subject with ID '{subject_id}'" in str(exc_info.value)

    # ========== Tests for execute_all_students_dashboard ==========

    def test_execute_all_students_dashboard_success(self, use_case, mock_student_repository, mock_grade_repository):
        students = [
            Student(
                id="S001",
                name="Juan",
                lastname="Pérez",
                email="juan@test.com",
                semester=5,
                average=85.0,
            ),
            Student(
                id="S002",
                name="María",
                lastname="García",
                email="maria@test.com",
                semester=5,
                average=90.0,
            ),
        ]

        mock_student_repository.get_all.return_value = students
        mock_grade_repository.is_regular_student.side_effect = [True, False]

        result = use_case.execute_all_students_dashboard(page_size=25, page=1, sort_field="name", sort_order="asc")

        assert len(result) == 2
        assert isinstance(result[0], StudentReportDashboard)
        assert result[0].id == "S001"
        assert result[0].name == "Juan"
        assert result[0].status is True
        assert result[1].id == "S002"
        assert result[1].status is False

        mock_student_repository.get_all.assert_called_once_with(page_size=25, page=1, sort_field="name", sort_order="asc")
        assert mock_grade_repository.is_regular_student.call_count == 2

    def test_execute_all_students_dashboard_empty_list(self, use_case, mock_student_repository):
        mock_student_repository.get_all.return_value = []

        result = use_case.execute_all_students_dashboard(page_size=25, page=1)

        assert result == []
        assert isinstance(result, list)
