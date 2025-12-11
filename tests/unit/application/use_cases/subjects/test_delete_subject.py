from unittest.mock import Mock

import pytest

from application.use_cases.subjects.update_subject import UpdateSubjectUseCase
from domain.entities.subject import Subject
from domain.exceptions.cannot_update_resource_exception import (
    CannotUpdateResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException


class TestUpdateSubjectUseCase:
    @pytest.fixture
    def mock_subject_repository(self):
        return Mock()

    @pytest.fixture
    def mock_student_repository(self):
        repo = Mock()
        repo.get_by_semester.return_value = []
        return Mock()

    @pytest.fixture
    def mock_profesor_repository(self):
        return Mock()

    @pytest.fixture
    def mock_grade_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_subject_repository, mock_grade_repository, mock_student_repository, mock_profesor_repository):
        return UpdateSubjectUseCase(mock_subject_repository, mock_grade_repository, mock_student_repository, mock_profesor_repository)

    @pytest.fixture
    def sample_subject_data(self):
        return Subject(
            id="MAT101",
            name="Matemáticas Avanzadas",
            description="Cálculo diferencial e integral",
            credits=4,
            semester=5,
            professor_id="PROF123",
        )

    def test_execute_success(self, use_case, mock_subject_repository, sample_subject_data):
        updated_subject = Subject(
            id="MAT101",
            name="Matemáticas Avanzadas",
            description="Cálculo diferencial e integral actualizado",
            credits=5,
            semester=6,
            professor_id="PROF123",
        )
        mock_subject_repository.get_by_id.return_value = sample_subject_data
        mock_subject_repository.update.return_value = updated_subject

        result = use_case.execute(sample_subject_data)

        assert result == updated_subject
        assert result.description == "Cálculo diferencial e integral actualizado"
        assert result.credits == 5
        assert result.semester == 6
        mock_subject_repository.get_by_id.assert_called_once_with(sample_subject_data.id)
        mock_subject_repository.update.assert_called_once_with(sample_subject_data)

    def test_execute_subject_not_found(self, use_case, mock_subject_repository, sample_subject_data):
        mock_subject_repository.get_by_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute(sample_subject_data)

        assert "Subject cannot be found by id" in str(exc_info.value)
        mock_subject_repository.get_by_id.assert_called_once_with(sample_subject_data.id)
        mock_subject_repository.update.assert_not_called()

    def test_execute_update_fails(self, use_case, mock_subject_repository, sample_subject_data):
        mock_subject_repository.get_by_id.return_value = sample_subject_data
        mock_subject_repository.update.return_value = None

        with pytest.raises(CannotUpdateResourceException) as exc_info:
            use_case.execute(sample_subject_data)

        assert "Subject cannot be updated" in str(exc_info.value)
        mock_subject_repository.get_by_id.assert_called_once_with(sample_subject_data.id)
        mock_subject_repository.update.assert_called_once_with(sample_subject_data)

    def test_execute_with_different_subject_ids(self, use_case, mock_subject_repository):
        subject_ids = ["MAT101", "FIS101", "QUI101", "BIO101"]

        for subject_id in subject_ids:
            subject_data = Subject(
                id=subject_id,
                name="Test Subject",
                description="Test Description",
                credits=4,
                semester=5,
                professor_id="PROF123",
            )
            updated_subject = Subject(
                id=subject_id,
                name="Test Subject Updated",
                description="Test Description",
                credits=4,
                semester=5,
                professor_id="PROF123",
            )
            mock_subject_repository.get_by_id.return_value = subject_data
            mock_subject_repository.update.return_value = updated_subject

            result = use_case.execute(subject_data)

            assert result.id == subject_id
            mock_subject_repository.get_by_id.assert_called_with(subject_id)
