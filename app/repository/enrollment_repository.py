from datetime import datetime, date
from app.extension import mongo
from pymongo.client_session import ClientSession
from bson import json_util, ObjectId
from flask import abort
import json

class EnrollmentRepository:
    @staticmethod
    def get_all_enrollments(session: ClientSession):
        try:
            enrollments = list(mongo.db.enrollments.find({}, session=session))
            return json.loads(json_util.dumps(enrollments))
        except Exception as e:
            raise e
    
    @staticmethod
    def get_enrollments_by_student(student_id: str, session: ClientSession):
        try:
            # Verify student exists
            student = mongo.db.students.find_one({"_id": ObjectId(student_id)}, session=session)
            if not student:
                abort(404, "Student not found")
                
            # Get enrollments
            enrollments = list(mongo.db.enrollments.find({"student_id": student_id}, session=session))
            return json.loads(json_util.dumps(enrollments))
        except Exception as e:
            raise e
    
    @staticmethod
    def get_enrollments_by_course(course_id: str, session: ClientSession):
        try:
            # Verify course exists
            course = mongo.db.courses.find_one({"_id": ObjectId(course_id)}, session=session)
            if not course:
                abort(404, "Course not found")
                
            # Get enrollments
            enrollments = list(mongo.db.enrollments.find({"course_id": course_id}, session=session))
            return json.loads(json_util.dumps(enrollments))
        except Exception as e:
            raise e
    
    @staticmethod
    def create_enrollment(args: dict, session: ClientSession):
        try:
            student = mongo.db.students.find_one({"_id": ObjectId(args["student_id"])}, session=session)
            if not student:
                abort(400, "Student not found")
                
            course = mongo.db.courses.find_one({"_id": ObjectId(args["course_id"])}, session=session)
            if not course:
                abort(400, "Course not found")
        
            existing = mongo.db.enrollments.find_one({
                "student_id": args["student_id"],
                "course_id": args["course_id"]
            }, session=session)
            
            if existing:
                abort(400, "Student is already enrolled in this course")
            
            if "max_students" in course and course["max_students"]:
                current_enrollments = mongo.db.enrollments.count_documents({
                    "course_id": args["course_id"]
                }, session=session)
                
                if current_enrollments >= course["max_students"]:
                    abort(400, "Course has reached maximum enrollment")
            
            args["status"] = "active"
            args["created_at"] = datetime.now()
            
            # No need for date conversion since we're using String
            # enrollment_date is already a string from the API
            
            # Convert to serializable format using json_util
            enrollment_doc = json.loads(json_util.dumps(args))
            
            result = mongo.db.enrollments.insert_one(enrollment_doc, session=session)
            return json.loads(json_util.dumps(result.inserted_id))
        except Exception as e:
            raise e
    
    @staticmethod
    def update_enrollment(enrollment_id: str, args: dict, session: ClientSession):
        try:
            # Add updated_at timestamp
            args["updated_at"] = datetime.now()
            
            result = mongo.db.enrollments.update_one(
                {"_id": ObjectId(enrollment_id)},
                {"$set": args},
                session=session
            )
            
            if result.matched_count == 0:
                abort(404, "Enrollment not found")
                
            return {"matched_count": result.matched_count, "modified_count": result.modified_count}
        except Exception as e:
            raise e
    
    @staticmethod
    def delete_enrollment(enrollment_id: str, session: ClientSession):
        try:
            # First check if enrollment exists
            enrollment = mongo.db.enrollments.find_one({"_id": ObjectId(enrollment_id)}, session=session)
            if not enrollment:
                abort(404, "Enrollment not found")
            
            # Then delete the enrollment
            result = mongo.db.enrollments.delete_one({"_id": ObjectId(enrollment_id)}, session=session)
            
            return {"deleted_count": result.deleted_count}
        except Exception as e:
            raise e
