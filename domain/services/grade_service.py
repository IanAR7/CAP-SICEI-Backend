class GradeService:
    def calculate_average(self, grades: list | None) -> float:
        if not grades:
            return 0.0
        total = sum(g.value for g in grades)
        return total / len(grades)
