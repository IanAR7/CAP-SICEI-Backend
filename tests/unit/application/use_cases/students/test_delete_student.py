from unittest.mock import Mock

import pytest

from application.use_cases.students.delete_student import DeleteStudentUseCase
from domain.exceptions.cannot_delete_resource_exception import (
    CannotDeleteResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException


class TestDeleteStudentUseCase:
    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_repository):
        return DeleteStudentUseCase(mock_repository)

    def test_execute_successful_deletion(self, use_case, mock_repository):
        student_id = "A25009999"
        mock_repository.exists.return_value = True
        mock_repository.delete.return_value = True

        use_case.execute(student_id)

        mock_repository.exists.assert_called_once_with(student_id)
        mock_repository.delete.assert_called_once_with(student_id)

    def test_execute_raises_resource_not_found_exception_when_student_does_not_exist(self, use_case, mock_repository):
        student_id = "nonexistent-student"
        mock_repository.exists.return_value = False

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute(student_id)

        assert exc_info.value.message == "Student cannot be found by id"
        mock_repository.exists.assert_called_once_with(student_id)
        mock_repository.delete.assert_not_called()

    def test_execute_raises_cannot_delete_resource_exception_when_deletion_fails(self, use_case, mock_repository):
        student_id = "A25009999"
        mock_repository.exists.return_value = True
        mock_repository.delete.return_value = False

        with pytest.raises(CannotDeleteResourceException) as exc_info:
            use_case.execute(student_id)

        assert exc_info.value.message == "Cannot delete student successfully"
        mock_repository.exists.assert_called_once_with(student_id)
        mock_repository.delete.assert_called_once_with(student_id)

    def test_execute_with_different_student_ids(self, use_case, mock_repository):
        student_ids = ["A25003545", "A25005656", "A25008237"]
        mock_repository.exists.return_value = True
        mock_repository.delete.return_value = True

        for student_id in student_ids:
            use_case.execute(student_id)
            mock_repository.exists.assert_called_with(student_id)
            mock_repository.delete.assert_called_with(student_id)
