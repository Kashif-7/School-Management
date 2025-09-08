from datetime import datetime
from app.extension import db
from app.model.models import Teacher, Course
from flask import abort
from sqlalchemy.exc import SQLAlchemyError

class TeacherRepository:
    @staticmethod
    def get_all_teachers():
        try:
            teachers = Teacher.query.all()
            return teachers
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_teacher_by_id(teacher_id: int):
        try:
            teacher = Teacher.query.get(teacher_id)
            if not teacher:
                abort(404, "Teacher not found")
            return teacher
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def create_teacher(args: dict):
        try:
            teacher = Teacher(
                first_name=args.get("first_name"),
                last_name=args.get("last_name"),
                email=args.get("email"),
                subject=args.get("subject"),
                qualification=args.get("qualification"),
                phone=args.get("phone")
            )
            
            db.session.add(teacher)
            db.session.commit()
            return teacher.id
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_teacher(teacher_id: int, args: dict):
        try:
            teacher = Teacher.query.get(teacher_id)
            if not teacher:
                abort(404, "Teacher not found")
            
            # Update teacher attributes
            if "first_name" in args:
                teacher.first_name = args["first_name"]
            if "last_name" in args:
                teacher.last_name = args["last_name"]
            if "email" in args:
                teacher.email = args["email"]
            if "subject" in args:
                teacher.subject = args["subject"]
            if "qualification" in args:
                teacher.qualification = args["qualification"]
            if "phone" in args:
                teacher.phone = args["phone"]
            
            db.session.commit()
            return {"teacher_id": teacher_id, "modified": True}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_teacher(teacher_id: int):
        try:
            teacher = Teacher.query.get(teacher_id)
            if not teacher:
                abort(404, "Teacher not found")
            
            # Check if teacher is assigned to any courses
            courses = Course.query.filter_by(teacher_id=teacher_id).all()
            if courses:
                abort(400, "Cannot delete teacher assigned to courses")
            
            db.session.delete(teacher)
            db.session.commit()
            return {"deleted": True}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
