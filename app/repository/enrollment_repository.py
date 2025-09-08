from datetime import datetime, date
from app.extension import db
from app.model.models import Enrollment, Student, Course
from flask import abort
from sqlalchemy.exc import SQLAlchemyError

class EnrollmentRepository:
    @staticmethod
    def get_all_enrollments():
        try:
            enrollments = Enrollment.query.all()
            return enrollments
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_enrollments_by_student(student_id: int):
        try:
            student = Student.query.get(student_id)
            if not student:
                abort(404, "Student not found")
                
            enrollments = Enrollment.query.filter_by(student_id=student_id).all()
            return enrollments
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_enrollments_by_course(course_id: int):
        try:
            course = Course.query.get(course_id)
            if not course:
                abort(404, "Course not found")
                
            enrollments = Enrollment.query.filter_by(course_id=course_id).all()
            return enrollments
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def create_enrollment(args: dict):
        try:
            # Check if student exists
            student = Student.query.get(args.get("student_id"))
            if not student:
                abort(400, "Student not found")
                
            # Check if course exists
            course = Course.query.get(args.get("course_id"))
            if not course:
                abort(400, "Course not found")
            
            # Check if student is already enrolled in this course
            existing = Enrollment.query.filter_by(
                student_id=args.get("student_id"),
                course_id=args.get("course_id")
            ).first()
            
            if existing:
                abort(400, "Student is already enrolled in this course")
            
            # Check if course has reached maximum enrollment
            if course.max_students:
                current_enrollments = Enrollment.query.filter_by(
                    course_id=args.get("course_id")
                ).count()
                
                if current_enrollments >= course.max_students:
                    abort(400, "Course has reached maximum enrollment")
            
            # Create new enrollment
            enrollment = Enrollment(
                student_id=args.get("student_id"),
                course_id=args.get("course_id"),
                enrollment_date=args.get("enrollment_date", date.today()),
                status=args.get("status", "active"),
                grade=args.get("grade")
            )
            
            db.session.add(enrollment)
            db.session.commit()
            return enrollment.id
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_enrollment(enrollment_id: int, args: dict):
        try:
            enrollment = Enrollment.query.get(enrollment_id)
            if not enrollment:
                abort(404, "Enrollment not found")
            
            # Update enrollment attributes
            if "status" in args:
                enrollment.status = args["status"]
            if "grade" in args:
                enrollment.grade = args["grade"]
            if "enrollment_date" in args:
                enrollment.enrollment_date = args["enrollment_date"]
            
            db.session.commit()
            return {"enrollment_id": enrollment_id, "modified": True}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_enrollment(enrollment_id: int):
        try:
            enrollment = Enrollment.query.get(enrollment_id)
            if not enrollment:
                abort(404, "Enrollment not found")
            
            db.session.delete(enrollment)
            db.session.commit()
            return {"deleted": True}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
