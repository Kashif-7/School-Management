from app.repository.student_repository import StudentRepository

class StudentBLC:
    @staticmethod
    def get_all_students():
        """Get all students."""
        students = StudentRepository.get_all_students()
        return students
    
    @staticmethod
    def get_student_by_id(student_id: int):
        """Get a student by ID."""
        student = StudentRepository.get_student_by_id(student_id)
        return student
    
    @staticmethod
    def create_student(args: dict):
        """Create a new student."""
        student_id = StudentRepository.create_student(args)
        return {"student_id": student_id, "message": "Student created successfully"}
    
    @staticmethod
    def update_student(student_id: int, args: dict):
        """Update a student's information."""
        result = StudentRepository.update_student(student_id, args)
        return {"student_id": student_id, "message": "Student updated successfully"}
    
    @staticmethod
    def delete_student(student_id: int):
        """Delete a student and their enrollments."""
        result = StudentRepository.delete_student(student_id)
        return {"student_id": student_id, "message": "Student deleted successfully"}
