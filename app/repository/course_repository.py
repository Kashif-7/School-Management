from datetime import datetime
from app.extension import mongo
from pymongo.client_session import ClientSession
from bson import json_util, ObjectId
from flask import abort
import json

class CourseRepository:
    @staticmethod
    def get_all_courses(session: ClientSession):
        try:
            courses = list(mongo.db.courses.find({}, session=session))
            return json.loads(json_util.dumps(courses))
        except Exception as e:
            raise e
    
    @staticmethod
    def get_course_by_id(course_id: str, session: ClientSession):
        try:
            course = mongo.db.courses.find_one({"_id": ObjectId(course_id)}, session=session)
            if not course:
                abort(404, "Course not found")
            return json.loads(json_util.dumps(course))
        except Exception as e:
            raise e
    
    @staticmethod
    def create_course(args: dict, session: ClientSession):
        try:
            teacher = mongo.db.teachers.find_one({"_id": ObjectId(args["teacher_id"])}, session=session)
            if not teacher:
                abort(400, "Teacher not found")
            
            args["created_at"] = datetime.now()
            
            result = mongo.db.courses.insert_one(args, session=session)
            return json.loads(json_util.dumps(result.inserted_id))
        except Exception as e:
            raise e
    
    @staticmethod
    def update_course(course_id: str, args: dict, session: ClientSession):
        try:

            if "teacher_id" in args:
                teacher = mongo.db.teachers.find_one({"_id": ObjectId(args["teacher_id"])}, session=session)
                if not teacher:
                    abort(400, "Teacher not found")
        
            args["updated_at"] = datetime.now()
            
            result = mongo.db.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": args},
                session=session
            )
            
            if result.matched_count == 0:
                abort(404, "Course not found")
                
            return {"matched_count": result.matched_count, "modified_count": result.modified_count}
        except Exception as e:
            raise e
    
    @staticmethod
    def delete_course(course_id: str, session: ClientSession):
        try:
            course = mongo.db.courses.find_one({"_id": ObjectId(course_id)}, session=session)
            if not course:
                abort(404, "Course not found")
            
            result = mongo.db.courses.delete_one({"_id": ObjectId(course_id)}, session=session)
            
            mongo.db.enrollments.delete_many({"course_id": course_id}, session=session)
            
            return {"deleted_count": result.deleted_count}
        except Exception as e:
            raise e
