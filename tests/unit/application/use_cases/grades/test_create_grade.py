from unittest.mock import Mock

import pytest

from application.use_cases.grades.create_grade import CreateGradeUseCase
from domain.entities.grade import Grade
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.not_enough_arguments_exception import NotEnoughArgumentsException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.grade_repository import GradeRepository
from domain.repositories.student_repository import StudentRepository
from domain.repositories.subject_repository import SubjectRepository


class TestCreateGradeUseCase:
    @pytest.fixture
    def mock_grade_repository(self):
        return Mock(spec=GradeRepository)

    @pytest.fixture
    def mock_student_repository(self):
        return Mock(spec=StudentRepository)

    @pytest.fixture
    def mock_subject_repository(self):
        return Mock(spec=SubjectRepository)

    @pytest.fixture
    def use_case(self, mock_grade_repository, mock_student_repository, mock_subject_repository):
        return CreateGradeUseCase(
            repository=mock_grade_repository,
            student_repository=mock_student_repository,
            subject_repository=mock_subject_repository,
        )

    @pytest.fixture
    def valid_grade_data(self):
        return Grade(id=None, student_id="A2500001", subject_id="MAT101", value=85.5)

    def test_execute_success(
        self,
        use_case,
        valid_grade_data,
        mock_student_repository,
        mock_subject_repository,
        mock_grade_repository,
    ):
        mock_student_repository.exists.return_value = True
        mock_subject_repository.exists.return_value = True
        expected_grade = Grade(id=1, student_id="A2500001", subject_id="MAT101", value=85.5)
        mock_grade_repository.create.return_value = expected_grade

        result = use_case.execute(valid_grade_data)

        assert result == expected_grade
        mock_student_repository.exists.assert_called_once_with("A2500001")
        mock_subject_repository.exists.assert_called_once_with("MAT101")
        mock_grade_repository.create.assert_called_once_with(valid_grade_data)

    def test_execute_missing_student_id(self, use_case, valid_grade_data):
        """Test that NotEnoughArgumentsException is raised when student_id is missing"""
        valid_grade_data.student_id = None

        with pytest.raises(NotEnoughArgumentsException) as exc_info:
            use_case.execute(valid_grade_data)
        assert "Student ID and Course ID are required" in str(exc_info.value)

    def test_execute_missing_subject_id(self, use_case, valid_grade_data):
        """Test that NotEnoughArgumentsException is raised when subject_id is missing"""
        valid_grade_data.subject_id = None

        with pytest.raises(NotEnoughArgumentsException) as exc_info:
            use_case.execute(valid_grade_data)
        assert "Student ID and Course ID are required" in str(exc_info.value)

    def test_execute_student_not_found(self, use_case, valid_grade_data, mock_student_repository):
        """Test that ResourceNotFoundException is raised when student doesn't exist"""
        mock_student_repository.exists.return_value = False

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute(valid_grade_data)
        assert f"Student with ID {valid_grade_data.student_id} not found" in str(exc_info.value)

    def test_execute_subject_not_found(
        self,
        use_case,
        valid_grade_data,
        mock_student_repository,
        mock_subject_repository,
    ):
        """Test that ResourceNotFoundException is raised when subject doesn't exist"""
        mock_student_repository.exists.return_value = True
        mock_subject_repository.exists.return_value = False

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute(valid_grade_data)
        assert f"Course with ID {valid_grade_data.subject_id} not found" in str(exc_info.value)

    def test_execute_repository_create_fails(
        self,
        use_case,
        valid_grade_data,
        mock_student_repository,
        mock_subject_repository,
        mock_grade_repository,
    ):
        """Test that CannotCreateException is raised when repository fails to create"""
        mock_student_repository.exists.return_value = True
        mock_subject_repository.exists.return_value = True
        mock_grade_repository.create.return_value = None

        with pytest.raises(CannotCreateException) as exc_info:
            use_case.execute(valid_grade_data)
        assert "Cannot create grade" in str(exc_info.value)
