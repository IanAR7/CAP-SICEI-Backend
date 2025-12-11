import pytest

from domain.entities.grade import Grade
from domain.services.grade_service import GradeService


class TestGradeService:
    @pytest.fixture
    def service(self):
        return GradeService()

    def test_calculate_average_with_grades(self, service):
        grades = [
            Grade(id=1, student_id="S001", subject_id="SUB001", value=80.0),
            Grade(id=2, student_id="S001", subject_id="SUB002", value=90.0),
            Grade(id=3, student_id="S001", subject_id="SUB003", value=85.0),
        ]

        result = service.calculate_average(grades)

        assert result == 85.0

    def test_calculate_average_with_valid_grades(self, service):
        grades = [
            Grade(id=1, student_id="A1", subject_id="M1", value=80),
            Grade(id=2, student_id="A1", subject_id="M2", value=90),
        ]

        result = service.calculate_average(grades)

        assert result == 85.0

    def test_calculate_average_empty_list(self, service):
        result = service.calculate_average([])
        assert result == 0.0

    def test_calculate_average_single_grade(self, service):
        grades = [
            Grade(id=1, student_id="A1", subject_id="M1", value=70),
        ]

        result = service.calculate_average(grades)

        assert result == 70.0

    def test_calculate_average_none(self, service):
        result = service.calculate_average(None)

        assert result == 0.0

    def test_calculate_average_with_decimal_values(self, service):
        grades = [
            Grade(id=1, student_id="A1", subject_id="M1", value=79.5),
            Grade(id=2, student_id="A1", subject_id="M2", value=80.5),
        ]

        result = service.calculate_average(grades)

        assert result == 80.0

    def test_calculate_average_with_negative_values(self, service):
        grades = [
            Grade(id=1, student_id="A1", subject_id="M1", value=-10),
            Grade(id=2, student_id="A1", subject_id="M2", value=20),
        ]

        result = service.calculate_average(grades)

        assert result == 5.0  # (-10 + 20) / 2
