import pytest
from unittest.mock import Mock
from application.use_cases.students.get_student import GetStudentUseCase
from domain.entities.student import Student
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException


class TestGetStudentUseCase:

    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_repository):
        return GetStudentUseCase(mock_repository)

    @pytest.fixture
    def sample_student(self):
        return Student(
            id="A2500001",
            name="John",
            lastname="Doe",
            email="john.doe@example.com",
            semester=5,
            average=8.5
        )

    @pytest.fixture
    def sample_students_list(self):
        return [
            Student(
                id="A25000001",
                name="John",
                lastname="Doe",
                email="john.doe@example.com",
                semester=5,
                average=8.5
            ),
            Student(
                id="A25000002",
                name="Jane",
                lastname="Smith",
                email="jane.smith@example.com",
                semester=5,
                average=9.0
            )
        ]

    def test_execute_by_id_success(self, use_case, mock_repository, sample_student):
        student_id = "A25000001"
        mock_repository.get_by_id.return_value = sample_student

        result = use_case.execute_by_id(student_id)

        assert result == sample_student
        mock_repository.get_by_id.assert_called_once_with(student_id)

    def test_execute_by_id_not_found(self, use_case, mock_repository):
        student_id = "nonexistent"
        mock_repository.get_by_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_id(student_id)

        assert str(exc_info.value) == "Student cannot be found by id"
        mock_repository.get_by_id.assert_called_once_with(student_id)

    def test_execute_by_id_with_empty_string(self, use_case, mock_repository):
        student_id = ""
        mock_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ResourceNotFoundException):
            use_case.execute_by_id(student_id)

        mock_repository.get_by_id.assert_called_once_with(student_id)

    def test_execute_by_semester_success(self, use_case, mock_repository, sample_students_list):
        semester = 5
        mock_repository.get_by_semester.return_value = sample_students_list

        result = use_case.execute_by_semester(semester)

        assert result == sample_students_list
        assert len(result) == 2
        mock_repository.get_by_semester.assert_called_once_with(semester)

    def test_execute_by_semester_not_found(self, use_case, mock_repository):
        semester = 10
        mock_repository.get_by_semester.return_value = []

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_semester(semester)

        assert str(exc_info.value) == "No students found by semester"
        mock_repository.get_by_semester.assert_called_once_with(semester)

    def test_execute_by_semester_with_negative_semester(self, use_case, mock_repository):
        semester = -1
        mock_repository.get_by_semester.return_value = []

        with pytest.raises(ResourceNotFoundException):
            use_case.execute_by_semester(semester)

        mock_repository.get_by_semester.assert_called_once_with(semester)


    def test_execute_by_semester_with_none_return(self, use_case, mock_repository):
        semester = 5
        mock_repository.get_by_semester.return_value = None

        with pytest.raises(ResourceNotFoundException):
            use_case.execute_by_semester(semester)