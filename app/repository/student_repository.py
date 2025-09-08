from datetime import datetime
from app.extension import db
from app.model.models import Student, Enrollment
from flask import abort
from sqlalchemy.exc import SQLAlchemyError

class StudentRepository:
    @staticmethod
    def get_all_students():
        """Get all students from the database."""
        try:
            students = Student.query.all()
            return students
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_student_by_id(student_id: int):
        """Get a student by ID."""
        try:
            student = Student.query.get(student_id)
            if not student:
                abort(404, "Student not found")
            return student
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def create_student(args: dict):
        """Create a new student."""
        try:
            student = Student(
                first_name=args.get("first_name"),
                last_name=args.get("last_name"),
                email=args.get("email"),
                date_of_birth=args.get("date_of_birth"),
                grade=args.get("grade"),
                address=args.get("address"),
                phone=args.get("phone")
            )
            
            db.session.add(student)
            db.session.commit()
            return student.id
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_student(student_id: int, args: dict):
        """Update a student."""
        try:
            student = Student.query.get(student_id)
            if not student:
                abort(404, "Student not found")
            
            # Update student attributes
            if "first_name" in args:
                student.first_name = args["first_name"]
            if "last_name" in args:
                student.last_name = args["last_name"]
            if "email" in args:
                student.email = args["email"]
            if "date_of_birth" in args:
                student.date_of_birth = args["date_of_birth"]
            if "grade" in args:
                student.grade = args["grade"]
            if "address" in args:
                student.address = args["address"]
            if "phone" in args:
                student.phone = args["phone"]
            
            db.session.commit()
            return {"student_id": student_id, "modified": True}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_student(student_id: int):
        """Delete a student and their enrollments."""
        try:
            student = Student.query.get(student_id)
            if not student:
                abort(404, "Student not found")
            
            # No need to delete enrollments separately - cascade will handle it
            db.session.delete(student)
            db.session.commit()
            return {"deleted": True}
            
            return {"deleted_count": result.deleted_count}
        except Exception as e:
            raise e
