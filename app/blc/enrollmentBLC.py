from pymongo.client_session import ClientSession
from app.repository.enrollment_repository import EnrollmentRepository
from bson import ObjectId

class EnrollmentBLC:
    @staticmethod
    def get_all_enrollments(session: ClientSession):
        enrollments = EnrollmentRepository.get_all_enrollments(session=session)
        return enrollments
    
    @staticmethod
    def get_enrollments_by_student(student_id: str, session: ClientSession):
        enrollments = EnrollmentRepository.get_enrollments_by_student(student_id, session=session)
        return enrollments
    
    @staticmethod
    def get_enrollments_by_course(course_id: str, session: ClientSession):
        enrollments = EnrollmentRepository.get_enrollments_by_course(course_id, session=session)
        return enrollments
    
    @staticmethod
    def create_enrollment(args: dict, session: ClientSession):
        enrollment_id = EnrollmentRepository.create_enrollment(args, session=session)
        return {"enrollment_id": enrollment_id, "message": "Enrollment created successfully"}
    
    @staticmethod
    def update_enrollment(enrollment_id: str, args: dict, session: ClientSession):
        enrollment = EnrollmentRepository.update_enrollment(enrollment_id, args, session=session)
        return {"enrollment_id": enrollment_id, "message": "Enrollment updated successfully"}
    
    @staticmethod
    def delete_enrollment(enrollment_id: str, session: ClientSession):
        result = EnrollmentRepository.delete_enrollment(enrollment_id, session=session)
        return {"enrollment_id": enrollment_id, "message": "Enrollment deleted successfully"}
