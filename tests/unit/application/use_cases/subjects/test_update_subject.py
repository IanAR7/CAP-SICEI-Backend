from unittest.mock import Mock

import pytest

from application.use_cases.subjects.delete_subject import DeleteSubjectUseCase
from domain.exceptions.cannot_delete_resource_exception import (
    CannotDeleteResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException


class TestDeleteSubjectUseCase:
    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_repository):
        return DeleteSubjectUseCase(mock_repository)

    # ========== Tests for execute ==========

    def test_execute_success(self, use_case, mock_repository):
        subject_id = "MAT101"
        mock_repository.exists.return_value = True
        mock_repository.delete.return_value = True

        use_case.execute(subject_id)

        mock_repository.exists.assert_called_once_with(subject_id)
        mock_repository.delete.assert_called_once_with(subject_id)

    def test_execute_subject_not_found(self, use_case, mock_repository):
        subject_id = "NONEXISTENT"
        mock_repository.exists.return_value = False

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute(subject_id)

        assert "Subject cannot be found by id" in str(exc_info.value)
        mock_repository.exists.assert_called_once_with(subject_id)
        mock_repository.delete.assert_not_called()

    def test_execute_delete_fails(self, use_case, mock_repository):
        subject_id = "MAT101"
        mock_repository.exists.return_value = True
        mock_repository.delete.return_value = False

        with pytest.raises(CannotDeleteResourceException) as exc_info:
            use_case.execute(subject_id)

        assert "Cannot delete subject successfully" in str(exc_info.value)
        mock_repository.exists.assert_called_once_with(subject_id)
        mock_repository.delete.assert_called_once_with(subject_id)

    def test_execute_no_return_value(self, use_case, mock_repository):
        subject_id = "MAT101"
        mock_repository.exists.return_value = True
        mock_repository.delete.return_value = True

        result = use_case.execute(subject_id)

        assert result is None
