from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.blc.userBLC import UserBLC
from webargs.flaskparser import use_args
from webargs import fields
import jwt
import datetime
import os

bp = Blueprint("user", __name__)


@bp.route("/signup", methods=["POST"])
@use_args(
    {"username": fields.String(required=False), "email": fields.String(), "password": fields.String()},
    location="json",
)
def user_signup(args: dict):
    user = UserBLC.user_signup(args=args)
    return jsonify(user)

@bp.route("/login", methods=["POST"])
@use_args(
    {"email": fields.String(), "password": fields.String()},
    location="json",
)
def user_login(args: dict):
    try:
        user = UserBLC.user_login(args=args)
        
        if user:
            secret_key = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
            token = jwt.encode(
                {
                    "email": user.get("email"),
                    "user_id": user.get("user_id"),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                },
                secret_key,
                algorithm="HS256"
            )
            return jsonify({
                "message": "Login successful",
                "access_token": token,
                "user": {
                    "id": user["user_id"],
                    "email": user["email"],
                    "username": user.get("username", "")
                }
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
    return jsonify({"error": "Invalid credentials"}), 401