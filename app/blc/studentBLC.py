from pymongo.client_session import ClientSession
from app.repository.student_repository import StudentRepository
from bson import ObjectId

class StudentBLC:
    @staticmethod
    def get_all_students(session: ClientSession):
        students = StudentRepository.get_all_students(session=session)
        return students
    
    @staticmethod
    def get_student_by_id(student_id: str, session: ClientSession):
        student = StudentRepository.get_student_by_id(student_id, session=session)
        return student
    
    @staticmethod
    def create_student(args: dict, session: ClientSession):
        student_id = StudentRepository.create_student(args, session=session)
        return {"student_id": student_id, "message": "Student created successfully"}
    
    @staticmethod
    def update_student(student_id: str, args: dict, session: ClientSession):
        student = StudentRepository.update_student(student_id, args, session=session)
        return {"student_id": student_id, "message": "Student updated successfully"}
    
    @staticmethod
    def delete_student(student_id: str, session: ClientSession):
        result = StudentRepository.delete_student(student_id, session=session)
        return {"student_id": student_id, "message": "Student deleted successfully"}
