from datetime import datetime
from app.extension import mongo
from pymongo.client_session import ClientSession
from bson import json_util, ObjectId
from flask import abort
import json

class StudentRepository:
    @staticmethod
    def get_all_students(session: ClientSession):
        try:
            students = list(mongo.db.students.find({}, session=session))
            return students
        except Exception as e:
            raise e
    
    @staticmethod
    def get_student_by_id(student_id: str, session: ClientSession):
        try:
            student = mongo.db.students.find_one({"_id": ObjectId(student_id)}, session=session)
            if not student:
                abort(404, "Student not found")
            return student
        except Exception as e:
            raise e
    
    @staticmethod
    def create_student(args: dict, session: ClientSession):
        try:
            # Add created_at timestamp
            args["created_at"] = datetime.now()
            
            # Convert the entire document using json_util to handle all date-related fields
            student_doc = json.loads(json_util.dumps(args))
            
            # Now insert the document with properly serialized dates
            result = mongo.db.students.insert_one(student_doc, session=session)
            return str(result.inserted_id)
        except Exception as e:
            raise e
    
    @staticmethod
    def update_student(student_id: str, args: dict, session: ClientSession):
        try:
            # Add updated_at timestamp
            args["updated_at"] = datetime.now()
            
            # Convert the entire document using json_util to handle all date-related fields
            update_doc = json.loads(json_util.dumps(args))
            
            result = mongo.db.students.update_one(
                {"_id": ObjectId(student_id)},
                {"$set": update_doc},
                session=session
            )
            
            if result.matched_count == 0:
                abort(404, "Student not found")
                
            return {"matched_count": result.matched_count, "modified_count": result.modified_count}
        except Exception as e:
            raise e
    
    @staticmethod
    def delete_student(student_id: str, session: ClientSession):
        try:
            # First check if student exists
            student = mongo.db.students.find_one({"_id": ObjectId(student_id)}, session=session)
            if not student:
                abort(404, "Student not found")
            
            # Then delete the student
            result = mongo.db.students.delete_one({"_id": ObjectId(student_id)}, session=session)
            
            # Delete related enrollments
            mongo.db.enrollments.delete_many({"student_id": student_id}, session=session)
            
            return {"deleted_count": result.deleted_count}
        except Exception as e:
            raise e
