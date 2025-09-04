from datetime import datetime
from app.extension import mongo
from pymongo.client_session import ClientSession
from bson import json_util, ObjectId
from flask import abort
import json

class TeacherRepository:
    @staticmethod
    def get_all_teachers(session: ClientSession):
        try:
            teachers = list(mongo.db.teachers.find({}, session=session))
            return json.loads(json_util.dumps(teachers))
        except Exception as e:
            raise e
    
    @staticmethod
    def get_teacher_by_id(teacher_id: str, session: ClientSession):
        try:
            teacher = mongo.db.teachers.find_one({"_id": ObjectId(teacher_id)}, session=session)
            if not teacher:
                abort(404, "Teacher not found")
            return json.loads(json_util.dumps(teacher))
        except Exception as e:
            raise e
    
    @staticmethod
    def create_teacher(args: dict, session: ClientSession):
        try:
            # Add created_at timestamp
            args["created_at"] = datetime.now()
            
            result = mongo.db.teachers.insert_one(args, session=session)
            return json.loads(json_util.dumps(result.inserted_id))
        except Exception as e:
            raise e
    
    @staticmethod
    def update_teacher(teacher_id: str, args: dict, session: ClientSession):
        try:
            # Add updated_at timestamp
            args["updated_at"] = datetime.now()
            
            result = mongo.db.teachers.update_one(
                {"_id": ObjectId(teacher_id)},
                {"$set": args},
                session=session
            )
            
            if result.matched_count == 0:
                abort(404, "Teacher not found")
                
            return {"matched_count": result.matched_count, "modified_count": result.modified_count}
        except Exception as e:
            raise e
    
    @staticmethod
    def delete_teacher(teacher_id: str, session: ClientSession):
        try:
            # First check if teacher exists
            teacher = mongo.db.teachers.find_one({"_id": ObjectId(teacher_id)}, session=session)
            if not teacher:
                abort(404, "Teacher not found")
            
            # Check if teacher is assigned to any courses
            courses = list(mongo.db.courses.find({"teacher_id": teacher_id}, session=session))
            if courses:
                abort(400, "Cannot delete teacher assigned to courses")
            
            # Then delete the teacher
            result = mongo.db.teachers.delete_one({"_id": ObjectId(teacher_id)}, session=session)
            
            return {"deleted_count": result.deleted_count}
        except Exception as e:
            raise e
