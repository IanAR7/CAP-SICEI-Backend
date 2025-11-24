from unittest.mock import Mock

import pytest

from application.use_cases.grades.get_grade import GetGradeUseCase
from domain.entities.grade import Grade, GradeToShowStudent, GradeToShowSubject
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException


class TestGetGradeUseCase:
    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_repository):
        return GetGradeUseCase(mock_repository)

    # ========== Tests for execute_by_id ==========

    def test_execute_by_id_success(self, use_case, mock_repository):
        expected_grade = Grade(id=1, student_id="A2500001", subject_id="SUB001", value=85.5)
        mock_repository.get_by_id.return_value = expected_grade

        result = use_case.execute_by_id(1)

        assert result == expected_grade
        mock_repository.get_by_id.assert_called_once_with(1)

    def test_execute_by_id_not_found(self, use_case, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_id(999)

        assert "Grade cannot be found by id" in str(exc_info.value)
        mock_repository.get_by_id.assert_called_once_with(999)

    # ========== Tests for execute_all ==========

    def test_execute_all_with_pagination(self, use_case, mock_repository):
        expected_grades = [
            Grade(id=1, student_id="A2500001", subject_id="SUB001", value=80.0),
            Grade(id=2, student_id="A2500001", subject_id="SUB002", value=90.0),
        ]
        mock_repository.get_all.return_value = expected_grades

        result = use_case.execute_all(page_size=25, page=1, sort_field="id", sort_order="asc")

        assert result == expected_grades
        mock_repository.get_all.assert_called_once_with(page_size=25, page=1, sort_field="id", sort_order="asc")

    def test_execute_all_empty_list(self, use_case, mock_repository):
        mock_repository.get_all.return_value = []

        result = use_case.execute_all(page_size=25, page=1)

        assert result == []
        assert isinstance(result, list)

    # ========== Tests for execute_by_student_id ==========

    def test_execute_by_student_id_success(self, use_case, mock_repository):
        expected_grades = [
            Grade(id=1, student_id="A2500001", subject_id="SUB001", value=80.0),
            Grade(id=2, student_id="A2500001", subject_id="SUB002", value=90.0),
        ]
        mock_repository.get_by_student_id.return_value = expected_grades

        result = use_case.execute_by_student_id("A2500001")

        assert result == expected_grades
        assert len(result) == 2
        mock_repository.get_by_student_id.assert_called_once_with("A2500001")

    def test_execute_by_student_id_not_found(self, use_case, mock_repository):
        mock_repository.get_by_student_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_student_id("A2500001")

        assert "No grades found for student with ID 'A2500001'" in str(exc_info.value)

    def test_execute_by_student_id_empty_list(self, use_case, mock_repository):
        mock_repository.get_by_student_id.return_value = []

        with pytest.raises(ResourceNotFoundException):
            use_case.execute_by_student_id("A2500001")

    # ========== Tests for execute_by_subject_id ==========

    def test_execute_by_subject_id_success(self, use_case, mock_repository):
        expected_grades = [
            Grade(id=1, student_id="A2500001", subject_id="SUB001", value=80.0),
            Grade(id=2, student_id="A2500002", subject_id="SUB001", value=75.0),
        ]
        mock_repository.get_by_subject_id.return_value = expected_grades

        result = use_case.execute_by_subject_id("SUB001")

        assert result == expected_grades
        assert len(result) == 2
        mock_repository.get_by_subject_id.assert_called_once_with("SUB001")

    def test_execute_by_subject_id_not_found(self, use_case, mock_repository):
        mock_repository.get_by_subject_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_subject_id("SUB999")

        assert "No grades found for subject with ID 'SUB999'" in str(exc_info.value)

    # ========== Tests for execute_get_grades_by_student_id ==========

    def test_execute_get_grades_by_student_id_success(self, use_case, mock_repository):
        expected_grades = [
            GradeToShowStudent(id=1, subject="Matemáticas", value=80.0),
            GradeToShowStudent(id=2, subject="Física", value=90.0),
        ]
        mock_repository.get_student_grades_to_show.return_value = expected_grades

        result = use_case.execute_get_grades_by_student_id("A2500001")

        assert result == expected_grades
        assert all(isinstance(g, GradeToShowStudent) for g in result)
        mock_repository.get_student_grades_to_show.assert_called_once_with("A2500001")

    def test_execute_get_grades_by_student_id_not_found(self, use_case, mock_repository):
        mock_repository.get_student_grades_to_show.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_get_grades_by_student_id("S999")

        assert "No grades found for student with ID 'S999'" in str(exc_info.value)

    # ========== Tests for execute_get_grades_by_subject_id ==========

    def test_execute_get_grades_by_subject_id_success(self, use_case, mock_repository):
        expected_grades = [
            GradeToShowSubject(id=1, student="Juan Pérez", value=80.0),
            GradeToShowSubject(id=2, student="María García", value=90.0),
        ]
        mock_repository.get_subject_grades_to_show.return_value = expected_grades

        result = use_case.execute_get_grades_by_subject_id("SUB001")

        assert result == expected_grades
        assert all(isinstance(g, GradeToShowSubject) for g in result)
        mock_repository.get_subject_grades_to_show.assert_called_once_with("SUB001")

    def test_execute_get_grades_by_subject_id_not_found(self, use_case, mock_repository):
        mock_repository.get_subject_grades_to_show.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_get_grades_by_subject_id("SUB999")

        assert "No grades found for subject with ID 'SUB999'" in str(exc_info.value)
