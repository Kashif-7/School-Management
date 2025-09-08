
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extension import db
from app.model.models import User
from flask import abort

class UserRepository:
    
    @staticmethod    
    def user_signup(args):
        try:
            # Create a new user with SQLAlchemy
            new_user = User(
                username=args.get("username", args["email"].split('@')[0]),  # Default username from email
                email=args["email"],
                password_hash=generate_password_hash(args["password"])
            )
            
            # Add to session and commit
            db.session.add(new_user)
            db.session.commit()
            
            return new_user.id

        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def user_login(args):
        # Find user by email
        user = User.query.filter_by(email=args["email"]).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password_hash, args["password"]):
            # No need to log failed logins in this version
            abort(401, "Invalid email or password")
        
        # Create user info dictionary to return
        user_info = {
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "created_at": user.created_at
        }
        
        # No need to log successful logins in this version
        
        return user_info
