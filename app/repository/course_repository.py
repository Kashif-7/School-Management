from datetime import datetime
from app.extension import db
from app.model.models import Course, Teacher, Enrollment
from flask import abort
from sqlalchemy.exc import SQLAlchemyError

class CourseRepository:
    @staticmethod
    def get_all_courses():
        try:
            courses = Course.query.all()
            return courses
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_course_by_id(course_id: int):
        try:
            course = Course.query.get(course_id)
            if not course:
                abort(404, "Course not found")
            return course
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def create_course(args: dict):
        try:
            # Check if teacher exists
            teacher = Teacher.query.get(args.get("teacher_id"))
            if not teacher:
                abort(400, "Teacher not found")
            
            course = Course(
                name=args.get("name"),
                description=args.get("description"),
                credits=args.get("credits"),
                max_students=args.get("max_students", 30),
                teacher_id=args.get("teacher_id")
            )
            
            db.session.add(course)
            db.session.commit()
            return course.id
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_course(course_id: int, args: dict):
        try:
            course = Course.query.get(course_id)
            if not course:
                abort(404, "Course not found")
                
            # Check if teacher exists if teacher_id is being updated
            if "teacher_id" in args:
                teacher = Teacher.query.get(args["teacher_id"])
                if not teacher:
                    abort(400, "Teacher not found")
                course.teacher_id = args["teacher_id"]
            
            # Update course attributes
            if "name" in args:
                course.name = args["name"]
            if "description" in args:
                course.description = args["description"]
            if "credits" in args:
                course.credits = args["credits"]
            if "max_students" in args:
                course.max_students = args["max_students"]
            
            db.session.commit()
            return {"course_id": course_id, "modified": True}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_course(course_id: int):
        try:
            course = Course.query.get(course_id)
            if not course:
                abort(404, "Course not found")
            
            # No need to delete enrollments separately - cascade will handle it
            db.session.delete(course)
            db.session.commit()
            return {"deleted": True}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
