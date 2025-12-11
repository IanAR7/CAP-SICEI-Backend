import random

from domain.entities.student import Student
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.repositories.student_repository import StudentRepository


class CreateStudentUseCase:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def execute(self, student_data: Student) -> Student:
        student_data.id = self.generate_student_id()

        created_student = self.repository.create(student_data)

        if not created_student:
            raise CannotCreateException("Cannot create student")

        return created_student

    def generate_student_id(self, year: int = 2025) -> str:
        prefix = f"A{str(year)[-2:]}00"
        random_digits = f"{random.randint(0, 9999):04d}"
        new_id = prefix + random_digits

        if self.repository.exists(new_id):
            return self.generate_student_id(year)

        return new_id
