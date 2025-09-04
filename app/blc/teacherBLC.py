from pymongo.client_session import ClientSession
from app.repository.teacher_repository import TeacherRepository
from bson import ObjectId

class TeacherBLC:
    @staticmethod
    def get_all_teachers(session: ClientSession):
        teachers = TeacherRepository.get_all_teachers(session=session)
        return teachers
    
    @staticmethod
    def get_teacher_by_id(teacher_id: str, session: ClientSession):
        teacher = TeacherRepository.get_teacher_by_id(teacher_id, session=session)
        return teacher
    
    @staticmethod
    def create_teacher(args: dict, session: ClientSession):
        teacher_id = TeacherRepository.create_teacher(args, session=session)
        return {"teacher_id": teacher_id, "message": "Teacher created successfully"}
    
    @staticmethod
    def update_teacher(teacher_id: str, args: dict, session: ClientSession):
        teacher = TeacherRepository.update_teacher(teacher_id, args, session=session)
        return {"teacher_id": teacher_id, "message": "Teacher updated successfully"}
    
    @staticmethod
    def delete_teacher(teacher_id: str, session: ClientSession):
        result = TeacherRepository.delete_teacher(teacher_id, session=session)
        return {"teacher_id": teacher_id, "message": "Teacher deleted successfully"}
