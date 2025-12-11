ALLOWED_STUDENT_SORT_FIELDS = {"id", "name", "lastname", "email", "semester"}
ALLOWED_SUBJECT_SORT_FIELDS = {"id", "name", "credits", "semester"}
ALLOWED_GRADES_SORT_FIELDS = {"id", "student_id", "subject_id", "grade"}
ALLOWED_ALERT_SORT_FIELDS = ["id", "title", "alert_type", "status", "created_at", "scheduled_at", "sent_at"]
ALLOWED_PROFESSOR_SORT_FIELDS = {"id", "name", "lastname", "email", "semester"}
ALLOWED_SORT_ORDERS = {"asc", "desc"}
