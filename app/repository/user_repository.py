
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extension import mongo
from pymongo.client_session import ClientSession
from bson import json_util
from flask import abort

import json
import pymongo

class UserRepository:
    
    @staticmethod    
    def user_signup(args, session: ClientSession):
        try:
            doc = mongo.db.users.insert_one(
                {
                    "email": args["email"],
                    "password": generate_password_hash(args["password"]),
                },
                session=session,
            )

            return json.loads(json_util.dumps(doc.inserted_id))

        except Exception as e:
            raise e
        
    @staticmethod
    def user_login(args, session: ClientSession):
            user = mongo.db.users.find_one(
                {"email": args["email"]}, session=session
            )
            if not user or not check_password_hash(user["password"], args["password"]):
                failed_login = {
                    "email": args["email"],
                    "login_time": datetime.now(),
                    "login_status": "failed",
                    "error_reason": "Invalid email or password"
                }
                try:
                    mongo.db.login_info.insert_one(failed_login, session=session)
                except:
                    pass  
                
                abort(401, "Invalid email or password")
            
           
            login_info = {
                "user_id": user["_id"],
                "email": user["email"],
                "login_time": datetime.now(),
                "login_status": "success"
            }
            
            mongo.db.login_info.insert_one(login_info, session=session)
            
            return user
            