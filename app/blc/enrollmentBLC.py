from app.repository.enrollment_repository import EnrollmentRepository

class EnrollmentBLC:
    @staticmethod
    def get_all_enrollments():
        enrollments = EnrollmentRepository.get_all_enrollments()
        return enrollments
    
    @staticmethod
    def get_enrollments_by_student(student_id: int):
        enrollments = EnrollmentRepository.get_enrollments_by_student(student_id)
        return enrollments
    
    @staticmethod
    def get_enrollments_by_course(course_id: int):
        enrollments = EnrollmentRepository.get_enrollments_by_course(course_id)
        return enrollments
    
    @staticmethod
    def create_enrollment(args: dict):
        enrollment_id = EnrollmentRepository.create_enrollment(args)
        return {"enrollment_id": enrollment_id, "message": "Enrollment created successfully"}
    
    @staticmethod
    def update_enrollment(enrollment_id: int, args: dict):
        enrollment = EnrollmentRepository.update_enrollment(enrollment_id, args)
        return {"enrollment_id": enrollment_id, "message": "Enrollment updated successfully"}
    
    @staticmethod
    def delete_enrollment(enrollment_id: int):
        result = EnrollmentRepository.delete_enrollment(enrollment_id)
        return {"enrollment_id": enrollment_id, "message": "Enrollment deleted successfully"}
