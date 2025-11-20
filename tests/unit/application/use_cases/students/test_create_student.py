from unittest.mock import Mock, patch

import pytest

from application.use_cases.students.create_student import CreateStudentUseCase
from domain.entities.student import Student
from domain.exceptions.cannot_create_exception import CannotCreateException


class TestCreateStudentUseCase:
    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_repository):
        return CreateStudentUseCase(mock_repository)

    @pytest.fixture
    def sample_student_data(self):
        return Student(
            id=None,
            name="John",
            lastname="Doe",
            email="john.doe@example.com",
            semester=5,
            average=8.5,
        )

    def test_successful_student_creation(self, use_case, mock_repository, sample_student_data):
        expected_student = Student(
            id="A25000001",
            name="John",
            lastname="Doe",
            email="john.doe@example.com",
            semester=5,
            average=8.5,
        )
        mock_repository.exists.return_value = False
        mock_repository.create.return_value = expected_student

        with patch("random.randint", return_value=1):
            result = use_case.execute(sample_student_data)

        assert result.id == "A25000001"
        assert result.name == "John"
        assert result.lastname == "Doe"
        assert result.email == "john.doe@example.com"
        assert result.semester == 5
        assert result.average == 8.5
        mock_repository.create.assert_called_once()
        mock_repository.exists.assert_called_once_with("A25000001")

    def test_id_generation_format(self, use_case, mock_repository):
        mock_repository.exists.return_value = False

        with patch("random.randint", return_value=1234):
            generated_id = use_case.generate_student_id(year=2025)

        assert generated_id == "A25001234"
        assert generated_id.startswith("A25")
        assert len(generated_id) == 9

    def test_id_generation_with_different_year(self, use_case, mock_repository):
        mock_repository.exists.return_value = False

        with patch("random.randint", return_value=5678):
            generated_id = use_case.generate_student_id(year=2024)

        assert generated_id == "A24005678"
        assert generated_id.startswith("A24")

    def test_id_generation_with_leading_zeros(self, use_case, mock_repository):
        mock_repository.exists.return_value = False

        with patch("random.randint", return_value=42):
            generated_id = use_case.generate_student_id(year=2025)

        assert generated_id == "A25000042"
        assert generated_id[5:] == "0042"

    def test_id_collision_handling_multiple_retries(self, use_case, mock_repository):
        mock_repository.exists.side_effect = [True, True, True, False]

        with patch("random.randint", side_effect=[1000, 1001, 1002, 1003]):
            generated_id = use_case.generate_student_id(year=2025)

        assert generated_id == "A25001003"
        assert mock_repository.exists.call_count == 4

    def test_repository_returns_none_raises_exception(self, use_case, mock_repository, sample_student_data):
        mock_repository.exists.return_value = False
        mock_repository.create.return_value = None

        with pytest.raises(CannotCreateException) as exc_info:
            with patch("random.randint", return_value=1234):
                use_case.execute(sample_student_data)

        assert str(exc_info.value) == "Cannot create student"
        mock_repository.create.assert_called_once()

    def test_student_id_is_assigned_before_creation(self, use_case, mock_repository, sample_student_data):
        mock_repository.exists.return_value = False
        created_student = Student(
            id="A25009999",
            name="John",
            lastname="Doe",
            email="john.doe@example.com",
            semester=5,
            average=8.5,
        )
        mock_repository.create.return_value = created_student

        # Act
        with patch("random.randint", return_value=9999):
            use_case.execute(sample_student_data)

        # Assert
        call_args = mock_repository.create.call_args[0][0]
        assert call_args.id == "A25009999"
        assert call_args.id is not None
