import pytest  
from unittest.mock import Mock  
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException  
from domain.exceptions.cannot_delete_resource_exception import CannotDeleteResourceException  
from application.use_cases.grades.delete_grade import DeleteGradeUseCase  
  
  
class TestDeleteGradeUseCase:  
      
    @pytest.fixture  
    def mock_repository(self):  
        return Mock()  
      
    @pytest.fixture  
    def use_case(self, mock_repository):  
        return DeleteGradeUseCase(mock_repository)  
      
    # ========== Tests para execute ==========  
      
    def test_execute_success(self, use_case, mock_repository):  
        grade_id = 1  
        mock_repository.exists.return_value = True  
        mock_repository.delete.return_value = True  
          
        use_case.execute(grade_id)  
          
        mock_repository.exists.assert_called_once_with(grade_id)  
        mock_repository.delete.assert_called_once_with(grade_id)  
      
    def test_execute_grade_not_found(self, use_case, mock_repository):  
        grade_id = 999  
        mock_repository.exists.return_value = False  
          
        with pytest.raises(ResourceNotFoundException) as exc_info:  
            use_case.execute(grade_id)  
          
        assert "Grade cannot be found by id" in str(exc_info.value)  
        mock_repository.exists.assert_called_once_with(grade_id)  
        mock_repository.delete.assert_not_called()  
      
    def test_execute_delete_fails(self, use_case, mock_repository):  
        grade_id = 1  
        mock_repository.exists.return_value = True  
        mock_repository.delete.return_value = False  
          
        with pytest.raises(CannotDeleteResourceException) as exc_info:  
            use_case.execute(grade_id)  
          
        assert "Cannot delete grade successfully" in str(exc_info.value)  
        mock_repository.exists.assert_called_once_with(grade_id)  
        mock_repository.delete.assert_called_once_with(grade_id)  
      
    def test_execute_with_different_grade_ids(self, use_case, mock_repository):  
        grade_ids = [1, 5, 10, 100]  
        mock_repository.exists.return_value = True  
        mock_repository.delete.return_value = True  
          
        for grade_id in grade_ids:  
            use_case.execute(grade_id)  
            mock_repository.exists.assert_called_with(grade_id)  
            mock_repository.delete.assert_called_with(grade_id)  
      
    def test_execute_no_return_value(self, use_case, mock_repository):  
        grade_id = 1  
        mock_repository.exists.return_value = True  
        mock_repository.delete.return_value = True  
          
        result = use_case.execute(grade_id)  
          
        assert result is None