import uuid
from unittest.mock import Mock, patch

import pytest

from application.use_cases.subjects.create_subject import CreateSubjectUseCase
from domain.entities.subject import Subject
from domain.exceptions.cannot_create_exception import CannotCreateException


class TestCreateSubjectUseCase:
    @pytest.fixture
    def mock_subject_repository(self):
        return Mock()

    @pytest.fixture
    def mock_profesor_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_subject_repository, mock_profesor_repository):
        return CreateSubjectUseCase(mock_subject_repository, mock_profesor_repository)

    @pytest.fixture
    def sample_subject_data(self):
        return Subject(id=None, name="Matemáticas", description="Cálculo diferencial", credits=4, semester=5, professor_id=5)

    # ========== Tests for execute ==========

    def test_execute_success(self, use_case, mock_subject_repository, sample_subject_data):
        generated_uuid = "550e8400-e29b-41d4-a716-446655440000"
        created_subject = Subject(id=generated_uuid, name="Matemáticas", description="Cálculo diferencial", credits=4, semester=5, professor_id=5)
        mock_subject_repository.exists.return_value = False
        mock_subject_repository.create.return_value = created_subject

        with patch("uuid.uuid4", return_value=uuid.UUID(generated_uuid)):
            result = use_case.execute(sample_subject_data)

        assert result == created_subject
        assert result.id == generated_uuid
        assert result.name == "Matemáticas"
        mock_subject_repository.exists.assert_called_once_with(generated_uuid)
        mock_subject_repository.create.assert_called_once()

        created_arg = mock_subject_repository.create.call_args[0][0]
        assert created_arg.id == generated_uuid

    def test_execute_create_fails(self, use_case, mock_subject_repository, sample_subject_data):
        generated_uuid = "550e8400-e29b-41d4-a716-446655440000"
        mock_subject_repository.exists.return_value = False
        mock_subject_repository.create.return_value = None

        with patch("uuid.uuid4", return_value=uuid.UUID(generated_uuid)):
            with pytest.raises(CannotCreateException) as exc_info:
                use_case.execute(sample_subject_data)

        assert "Cannot create subject successfully" in str(exc_info.value)
        mock_subject_repository.create.assert_called_once()

    def test_execute_assigns_id_before_creation(self, use_case, mock_subject_repository, sample_subject_data):
        generated_uuid = "123e4567-e89b-12d3-a456-426614174000"
        created_subject = Subject(id=generated_uuid, name="Matemáticas", description="Cálculo diferencial", credits=4, semester=5, professor_id=5)
        mock_subject_repository.exists.return_value = False
        mock_subject_repository.create.return_value = created_subject

        with patch("uuid.uuid4", return_value=uuid.UUID(generated_uuid)):
            use_case.execute(sample_subject_data)

        call_args = mock_subject_repository.create.call_args[0][0]
        assert call_args.id == generated_uuid
        assert call_args.id is not None

    # ========== Tests for generate_subject_id ==========

    def test_generate_subject_id_collision_single_retry(self, use_case, mock_subject_repository):
        first_uuid = "11111111-1111-1111-1111-111111111111"
        second_uuid = "22222222-2222-2222-2222-222222222222"
        mock_subject_repository.exists.side_effect = [
            True,
            False,
        ]  # First exists, second does not

        with patch("uuid.uuid4", side_effect=[uuid.UUID(first_uuid), uuid.UUID(second_uuid)]):
            generated_id = use_case.generate_subject_id()

        assert generated_id == second_uuid
        assert mock_subject_repository.exists.call_count == 2
        mock_subject_repository.exists.assert_any_call(first_uuid)
        mock_subject_repository.exists.assert_any_call(second_uuid)

    def test_generate_subject_id_recursion(self, use_case, mock_subject_repository):
        first_uuid = "12345678-1234-1234-1234-123456789012"
        second_uuid = "98765432-9876-9876-9876-987654321098"
        mock_subject_repository.exists.side_effect = [True, False]

        with patch("uuid.uuid4", side_effect=[uuid.UUID(first_uuid), uuid.UUID(second_uuid)]):
            result = use_case.generate_subject_id()

        assert result == second_uuid
        assert mock_subject_repository.exists.call_count == 2
