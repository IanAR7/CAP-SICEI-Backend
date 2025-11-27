from domain.repositories.student_repository import StudentRepository
from domain.repositories.subject_repository import SubjectRepository
from domain.repositories.grade_repository import GradeRepository
from domain.entities.student import Student
from domain.entities.grade import Grade
from domain.exceptions.cannot_update_resource_exception import CannotUpdateResourceException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException

class UpdateStudentUseCase:
    def __init__(
            self,
            student_repository: StudentRepository,
            subject_repository: SubjectRepository,
            grade_repository: GradeRepository
    ):
        self.student_repository = student_repository
        self.subject_repository = subject_repository
        self.grade_repository = grade_repository

    def execute(self, student_data: Student) -> Student:

        current_student = self.student_repository.get_by_id(student_data.id)
        if not current_student:
            raise ResourceNotFoundException("Student cannot be found by id")

        new_semester = student_data.semester

        if new_semester is not None and new_semester != current_student.semester:

            self.grade_repository.delete_by_student_id(current_student.id)

            updated_student = self.student_repository.update(student_data)

            if not updated_student:
                raise CannotUpdateResourceException("Student cannot be updated")

            new_subjects = self.subject_repository.get_by_semester(new_semester)

            for subject in new_subjects:
                new_grade = Grade(
                    id=None,
                    student_id=current_student.id,
                    subject_id=subject.id,
                    value=0.0
                )
                self.grade_repository.create(new_grade)

            return updated_student

        updated_student = self.student_repository.update(student_data)

        if not updated_student:
           raise CannotUpdateResourceException("Student cannot be updated")

        return updated_student