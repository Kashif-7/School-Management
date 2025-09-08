from app.repository.teacher_repository import TeacherRepository

class TeacherBLC:
    @staticmethod
    def get_all_teachers():
        teachers = TeacherRepository.get_all_teachers()
        return teachers
    
    @staticmethod
    def get_teacher_by_id(teacher_id: int):
        teacher = TeacherRepository.get_teacher_by_id(teacher_id)
        return teacher
    
    @staticmethod
    def create_teacher(args: dict):
        teacher_id = TeacherRepository.create_teacher(args)
        return {"teacher_id": teacher_id, "message": "Teacher created successfully"}
    
    @staticmethod
    def update_teacher(teacher_id: int, args: dict):
        teacher = TeacherRepository.update_teacher(teacher_id, args)
        return {"teacher_id": teacher_id, "message": "Teacher updated successfully"}
    
    @staticmethod
    def delete_teacher(teacher_id: int):
        result = TeacherRepository.delete_teacher(teacher_id)
        return {"teacher_id": teacher_id, "message": "Teacher deleted successfully"}
