from unittest.mock import Mock

import pytest

from application.use_cases.students.update_student import UpdateStudentUseCase
from domain.entities.student import Student
from domain.exceptions.cannot_update_resource_exception import (
    CannotUpdateResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException


class TestUpdateStudentUseCase:
    @pytest.fixture
    def mock_student_repository(self):
        return Mock()

    @pytest.fixture
    def mock_subject_repository(self):
        repo = Mock()
        repo.get_by_semester.return_value = []
        return Mock()

    @pytest.fixture
    def mock_grade_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_student_repository, mock_subject_repository, mock_grade_repository):
        return UpdateStudentUseCase(mock_student_repository, mock_subject_repository, mock_grade_repository)

    @pytest.fixture
    def sample_student_data(self):
        return Student(
            id="A25000001",
            name="Juan",
            lastname="Pérez",
            email="juan.perez@example.com",
            semester=5,
            average=85.0,
        )

    # ========== Tests para execute ==========

    def test_execute_success(self, use_case, mock_student_repository, sample_student_data):
        updated_student = Student(
            id="A25000001",
            name="Juan",
            lastname="Pérez García",
            email="juan.perez@example.com",
            semester=6,
            average=87.5,
        )

        mock_student_repository.get_by_id.return_value = sample_student_data
        mock_student_repository.update.return_value = updated_student

        result = use_case.execute(sample_student_data)

        assert result == updated_student

        mock_student_repository.get_by_id.assert_called_once_with(sample_student_data.id)
        mock_student_repository.update.assert_called_once_with(sample_student_data)

    def test_execute_student_not_found(self, use_case, mock_student_repository, sample_student_data):
        mock_student_repository.get_by_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute(sample_student_data)

        assert "Student cannot be found by id" in str(exc_info.value)
        mock_student_repository.get_by_id.assert_called_once_with(sample_student_data.id)
        mock_student_repository.update.assert_not_called()

    def test_execute_update_fails(self, use_case, mock_student_repository, sample_student_data):
        mock_student_repository.get_by_id.return_value = sample_student_data
        mock_student_repository.update.return_value = None

        with pytest.raises(CannotUpdateResourceException) as exc_info:
            use_case.execute(sample_student_data)

        assert "Student cannot be updated" in str(exc_info.value)
        mock_student_repository.get_by_id.assert_called_once_with(sample_student_data.id)
        mock_student_repository.update.assert_called_once_with(sample_student_data)

    def test_execute_partial_update(self, use_case, mock_student_repository):
        partial_student = Student(
            id="A25000001",
            name="Juan",
            lastname="Pérez",
            email="nuevo.email@example.com",
            semester=5,
            average=85.0,
        )
        updated_student = Student(
            id="S001",
            name="Juan",
            lastname="Pérez",
            email="nuevo.email@example.com",
            semester=5,
            average=85.0,
        )
        mock_student_repository.get_by_id.return_value = partial_student
        mock_student_repository.update.return_value = updated_student

        result = use_case.execute(partial_student)

        assert result.email == "nuevo.email@example.com"
        assert result.id == "S001"
        mock_student_repository.update.assert_called_once_with(partial_student)
