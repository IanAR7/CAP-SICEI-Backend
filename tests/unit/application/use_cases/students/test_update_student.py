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
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_repository):
        return UpdateStudentUseCase(mock_repository)

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

    def test_execute_success(self, use_case, mock_repository, sample_student_data):
        updated_student = Student(
            id="A25000001",
            name="Juan",
            lastname="Pérez García",
            email="juan.perez@example.com",
            semester=6,
            average=87.5,
        )
        mock_repository.exists.return_value = True
        mock_repository.update.return_value = updated_student

        result = use_case.execute(sample_student_data)

        assert result == updated_student
        assert result.lastname == "Pérez García"
        assert result.semester == 6
        mock_repository.exists.assert_called_once_with(sample_student_data.id)
        mock_repository.update.assert_called_once_with(sample_student_data)

    def test_execute_student_not_found(self, use_case, mock_repository, sample_student_data):
        mock_repository.exists.return_value = False

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute(sample_student_data)

        assert "Student cannot be found by id" in str(exc_info.value)
        mock_repository.exists.assert_called_once_with(sample_student_data.id)
        mock_repository.update.assert_not_called()

    def test_execute_update_fails(self, use_case, mock_repository, sample_student_data):
        mock_repository.exists.return_value = True
        mock_repository.update.return_value = None

        with pytest.raises(CannotUpdateResourceException) as exc_info:
            use_case.execute(sample_student_data)

        assert "Student cannot be updated" in str(exc_info.value)
        mock_repository.exists.assert_called_once_with(sample_student_data.id)
        mock_repository.update.assert_called_once_with(sample_student_data)

    def test_execute_partial_update(self, use_case, mock_repository):
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
        mock_repository.exists.return_value = True
        mock_repository.update.return_value = updated_student

        result = use_case.execute(partial_student)

        assert result.email == "nuevo.email@example.com"
        assert result.id == "S001"
        mock_repository.update.assert_called_once_with(partial_student)
