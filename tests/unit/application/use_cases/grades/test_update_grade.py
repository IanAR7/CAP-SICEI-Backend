from unittest.mock import Mock

import pytest

from application.use_cases.grades.update_grade import UpdateGradeUseCase
from domain.entities.grade import Grade
from domain.entities.student import Student
from domain.exceptions.cannot_update_resource_exception import (
    CannotUpdateResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException


class TestUpdateGradeUseCase:
    @pytest.fixture
    def mock_grade_repository(self):
        return Mock()

    @pytest.fixture
    def mock_student_repository(self):
        return Mock()

    @pytest.fixture
    def mock_grade_service(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_grade_repository, mock_student_repository, mock_grade_service):
        return UpdateGradeUseCase(
            grade_repository=mock_grade_repository,
            student_repository=mock_student_repository,
            grade_service=mock_grade_service,
        )

    @pytest.fixture
    def sample_grade_data(self):
        return Grade(id=1, student_id="S12345", subject_id="MATH101", value=85.5)

    @pytest.fixture
    def sample_student(self):
        return Student(
            id="S12345",
            name="John",
            lastname="Doe",
            email="john.doe@example.com",
            semester=3,
            average=80.0,
        )

    def test_execute_success(
        self,
        use_case,
        mock_grade_repository,
        mock_student_repository,
        mock_grade_service,
        sample_grade_data,
        sample_student,
    ):
        updated_grade = Grade(id=1, student_id="S12345", subject_id="MATH101", value=85.5)

        all_student_grades = [
            Grade(id=1, student_id="S12345", subject_id="MATH101", value=85.5),
            Grade(id=2, student_id="S12345", subject_id="ENG101", value=90.0),
            Grade(id=3, student_id="S12345", subject_id="PHYS101", value=88.0),
        ]

        new_average = 87.83

        mock_grade_repository.exists.return_value = True
        mock_grade_repository.update.return_value = updated_grade
        mock_grade_repository.get_by_student_id.return_value = all_student_grades
        mock_grade_service.calculate_average.return_value = new_average
        mock_student_repository.get_by_id.return_value = sample_student

        result = use_case.execute(sample_grade_data)

        assert result == updated_grade
        mock_grade_repository.exists.assert_called_once_with(sample_grade_data.id)
        mock_grade_repository.update.assert_called_once_with(sample_grade_data)
        mock_grade_repository.get_by_student_id.assert_called_once_with(updated_grade.student_id)
        mock_grade_service.calculate_average.assert_called_once_with(all_student_grades)
        mock_student_repository.get_by_id.assert_called_once_with(updated_grade.student_id)
        mock_student_repository.update.assert_called_once()

        # Verify student average was updated
        updated_student_call = mock_student_repository.update.call_args[0][0]
        assert updated_student_call.average == new_average

    def test_execute_grade_not_found(self, use_case, mock_grade_repository, sample_grade_data):
        """Test that ResourceNotFoundException is raised when grade doesn't exist"""
        mock_grade_repository.exists.return_value = False

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute(sample_grade_data)

        assert str(exc_info.value) == "Grade cannot be found by id"
        mock_grade_repository.exists.assert_called_once_with(sample_grade_data.id)
        mock_grade_repository.update.assert_not_called()

    def test_execute_update_failed(self, use_case, mock_grade_repository, sample_grade_data):
        """Test that CannotUpdateResourceException is raised when update fails"""
        mock_grade_repository.exists.return_value = True
        mock_grade_repository.update.return_value = None

        with pytest.raises(CannotUpdateResourceException) as exc_info:
            use_case.execute(sample_grade_data)

        assert str(exc_info.value) == "Grade cannot be updated"
        mock_grade_repository.exists.assert_called_once_with(sample_grade_data.id)
        mock_grade_repository.update.assert_called_once_with(sample_grade_data)

    def test_execute_cascade_update_logic(
        self,
        use_case,
        mock_grade_repository,
        mock_student_repository,
        mock_grade_service,
        sample_grade_data,
        sample_student,
    ):
        """Test that cascade update correctly recalculates student average"""
        updated_grade = Grade(id=1, student_id="S12345", subject_id="MATH101", value=95.0)

        all_student_grades = [
            Grade(id=1, student_id="S12345", subject_id="MATH101", value=95.0),
            Grade(id=2, student_id="S12345", subject_id="ENG101", value=85.0),
        ]

        new_average = 90.0

        mock_grade_repository.exists.return_value = True
        mock_grade_repository.update.return_value = updated_grade
        mock_grade_repository.get_by_student_id.return_value = all_student_grades
        mock_grade_service.calculate_average.return_value = new_average
        mock_student_repository.get_by_id.return_value = sample_student

        result = use_case.execute(sample_grade_data)

        assert result == updated_grade

        # Verify grade was retrieved for the correct student
        mock_grade_repository.get_by_student_id.assert_called_once_with("S12345")

        # Verify average calculation was called with all grades
        mock_grade_service.calculate_average.assert_called_once_with(all_student_grades)

        # Verify student was retrieved and updated
        mock_student_repository.get_by_id.assert_called_once_with("S12345")
        mock_student_repository.update.assert_called_once()

        # Verify the student's average was correctly updated
        updated_student = mock_student_repository.update.call_args[0][0]
        assert updated_student.id == "S12345"
        assert updated_student.average == 90.0

    def test_execute_with_zero_average(
        self,
        use_case,
        mock_grade_repository,
        mock_student_repository,
        mock_grade_service,
        sample_grade_data,
        sample_student,
    ):
        """Test update when calculated average is zero"""
        updated_grade = Grade(id=1, student_id="S12345", subject_id="MATH101", value=0.0)

        all_student_grades = [
            Grade(id=1, student_id="S12345", subject_id="MATH101", value=0.0),
        ]

        mock_grade_repository.exists.return_value = True
        mock_grade_repository.update.return_value = updated_grade
        mock_grade_repository.get_by_student_id.return_value = all_student_grades
        mock_grade_service.calculate_average.return_value = 0.0
        mock_student_repository.get_by_id.return_value = sample_student

        result = use_case.execute(sample_grade_data)

        assert result == updated_grade
        updated_student = mock_student_repository.update.call_args[0][0]
        assert updated_student.average == 0.0
