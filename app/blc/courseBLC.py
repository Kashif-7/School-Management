from pymongo.client_session import ClientSession
from app.repository.course_repository import CourseRepository
from bson import ObjectId

class CourseBLC:
    @staticmethod
    def get_all_courses(session: ClientSession):
        courses = CourseRepository.get_all_courses(session=session)
        return courses
    
    @staticmethod
    def get_course_by_id(course_id: str, session: ClientSession):
        course = CourseRepository.get_course_by_id(course_id, session=session)
        return course
    
    @staticmethod
    def create_course(args: dict, session: ClientSession):
        course_id = CourseRepository.create_course(args, session=session)
        return {"course_id": course_id, "message": "Course created successfully"}
    
    @staticmethod
    def update_course(course_id: str, args: dict, session: ClientSession):
        course = CourseRepository.update_course(course_id, args, session=session)
        return {"course_id": course_id, "message": "Course updated successfully"}
    
    @staticmethod
    def delete_course(course_id: str, session: ClientSession):
        result = CourseRepository.delete_course(course_id, session=session)
        return {"course_id": course_id, "message": "Course deleted successfully"}
