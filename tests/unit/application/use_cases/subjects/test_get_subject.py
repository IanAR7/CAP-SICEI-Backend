import pytest
from unittest.mock import Mock

from domain.entities.subject import Subject
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from application.use_cases.subjects.get_subject import GetSubjectUseCase


class TestGetSubjectUseCase:

    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_repository):
        return GetSubjectUseCase(mock_repository)

    @pytest.fixture
    def sample_subject(self):
        return Subject(
            id="MAT101",
            name="Matemáticas",
            description="Cálculo diferencial",
            credits=4,
            semester=5
        )

    @pytest.fixture
    def sample_subjects_list(self):
        return [
            Subject(
                id="MAT101",
                name="Matemáticas",
                description="Cálculo diferencial",
                credits=4,
                semester=5
            ),
            Subject(
                id="FIS101",
                name="Física",
                description="Mecánica clásica",
                credits=4,
                semester=5
            )
        ]

    # ========== Tests for execute_by_id ==========

    def test_execute_by_id_success(self, use_case, mock_repository, sample_subject):
        subject_id = "MAT101"
        mock_repository.get_by_id.return_value = sample_subject

        result = use_case.execute_by_id(subject_id)

        assert result == sample_subject
        assert result.id == "MAT101"
        assert result.name == "Matemáticas"
        mock_repository.get_by_id.assert_called_once_with(subject_id)

    def test_execute_by_id_not_found(self, use_case, mock_repository):
        subject_id = "NONEXISTENT"
        mock_repository.get_by_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_id(subject_id)

        assert "Subject cannot be found by id" in str(exc_info.value)
        mock_repository.get_by_id.assert_called_once_with(subject_id)

    def test_execute_by_id_with_empty_string(self, use_case, mock_repository):
        subject_id = ""
        mock_repository.get_by_id.return_value = None

        with pytest.raises(ResourceNotFoundException):
            use_case.execute_by_id(subject_id)

        mock_repository.get_by_id.assert_called_once_with(subject_id)

    # ========== Tests for execute_by_semester ==========

    def test_execute_by_semester_success(self, use_case, mock_repository, sample_subjects_list):
        semester = 5
        mock_repository.get_by_semester.return_value = sample_subjects_list

        result = use_case.execute_by_semester(semester)

        assert result == sample_subjects_list
        assert len(result) == 2
        assert all(s.semester == 5 for s in result)
        mock_repository.get_by_semester.assert_called_once_with(semester)

    def test_execute_by_semester_not_found(self, use_case, mock_repository):
        semester = 10
        mock_repository.get_by_semester.return_value = []

        with pytest.raises(ResourceNotFoundException) as exc_info:
            use_case.execute_by_semester(semester)

        assert "Subject cannot be found by id" in str(exc_info.value)
        mock_repository.get_by_semester.assert_called_once_with(semester)

    def test_execute_by_semester_with_none_return(self, use_case, mock_repository):
        semester = 5
        mock_repository.get_by_semester.return_value = None

        with pytest.raises(ResourceNotFoundException):
            use_case.execute_by_semester(semester)

    def test_execute_by_semester_with_negative_semester(self, use_case, mock_repository):
        semester = -1
        mock_repository.get_by_semester.return_value = []

        with pytest.raises(ResourceNotFoundException):
            use_case.execute_by_semester(semester)

        mock_repository.get_by_semester.assert_called_once_with(semester)

    # ========== Tests for execute_all ==========

    def test_execute_all_success(self, use_case, mock_repository, sample_subjects_list):
        page_size = 10
        page = 1
        mock_repository.get_all.return_value = sample_subjects_list

        result = use_case.execute_all(page_size=page_size, page=page)

        assert result == sample_subjects_list
        assert len(result) == 2
        mock_repository.get_all.assert_called_once_with(
            page_size=page_size,
            page=page,
            sort_field=None,
            sort_order=None
        )

    def test_execute_all_with_different_page_sizes(self, use_case, mock_repository, sample_subjects_list):
        page_size = 5
        page = 2
        mock_repository.get_all.return_value = sample_subjects_list

        result = use_case.execute_all(page_size=page_size, page=page)

        assert result == sample_subjects_list
        mock_repository.get_all.assert_called_once_with(
            page_size=page_size,
            page=page,
            sort_field=None,
            sort_order=None
        )

    def test_execute_all_with_descending_order(self, use_case, mock_repository, sample_subjects_list):
        page_size = 10
        page = 1
        sort_field = "credits"
        sort_order = "desc"
        mock_repository.get_all.return_value = sample_subjects_list

        # Act
        result = use_case.execute_all(
            page_size=page_size,
            page=page,
            sort_field=sort_field,
            sort_order=sort_order
        )

        # Assert
        assert result == sample_subjects_list
        mock_repository.get_all.assert_called_once_with(
            page_size=page_size,
            page=page,
            sort_field=sort_field,
            sort_order=sort_order
        )