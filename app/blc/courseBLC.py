from app.repository.course_repository import CourseRepository

class CourseBLC:
    @staticmethod
    def get_all_courses():
        courses = CourseRepository.get_all_courses()
        return courses
    
    @staticmethod
    def get_course_by_id(course_id: int):
        course = CourseRepository.get_course_by_id(course_id)
        return course
    
    @staticmethod
    def create_course(args: dict):
        course_id = CourseRepository.create_course(args)
        return {"course_id": course_id, "message": "Course created successfully"}
    
    @staticmethod
    def update_course(course_id: int, args: dict):
        course = CourseRepository.update_course(course_id, args)
        return {"course_id": course_id, "message": "Course updated successfully"}
    
    @staticmethod
    def delete_course(course_id: int):
        result = CourseRepository.delete_course(course_id)
        return {"course_id": course_id, "message": "Course deleted successfully"}
