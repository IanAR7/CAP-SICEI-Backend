from domain.repositories.subject_repository import SubjectRepository
from domain.repositories.grade_repository import GradeRepository
from domain.repositories.student_repository import StudentRepository
from domain.entities.subject import Subject
from domain.entities.grade import Grade
from domain.exceptions.cannot_update_resource_exception import CannotUpdateResourceException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException

class UpdateSubjectUseCase:
    def __init__(
            self,
            subject_repository: SubjectRepository,
            grade_repository: GradeRepository,
            student_repository: StudentRepository
    ):
        self.subject_repository = subject_repository
        self.grade_repository = grade_repository
        self.student_repository = student_repository

    def execute(self, subject_data: Subject) -> Subject:

        current_subject = self.subject_repository.get_by_id(subject_data.id)
        if not current_subject:
            raise ResourceNotFoundException("Subject cannot be found by id")

        new_semester = subject_data.semester

        if new_semester is not None and new_semester != current_subject.semester:

            self.grade_repository.delete_by_subject_id(current_subject.id)

            updated_subject = self.subject_repository.update(subject_data)

            if not updated_subject:
                raise CannotUpdateResourceException("Subject cannot be updated")

            students_in_new_semester = self.student_repository.get_by_semester(new_semester)

            for student in students_in_new_semester:
                new_grade = Grade(
                    id=None,
                    student_id=student.id,
                    subject_id=current_subject.id,
                    value=0.0
                )
                self.grade_repository.create(new_grade)

            return updated_subject

        updated_subject = self.subject_repository.update(subject_data)

        if not updated_subject:
           raise CannotUpdateResourceException("Subject cannot be updated")

        return updated_subject