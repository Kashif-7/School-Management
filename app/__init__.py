from flask import Flask, jsonify
from flask.json.provider import JSONProvider
from flask_cors import CORS
from app.extension import db, migrate
from app.api.root import bp as root_bp
from app.api.user import bp as user_bp
from app.api.student import bp as student_bp
from app.api.teacher import bp as teacher_bp
from app.api.course import bp as course_bp
from app.api.enrollment import bp as enrollment_bp
import datetime
import json
import os
from flask_sqlalchemy import SQLAlchemy


# Custom JSON provider to handle datetime and date objects
class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, default=self.default, **kwargs)
    
    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)
    
    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

app = Flask(__name__)
CORS(app)

app.json = CustomJSONProvider(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/school_management'

db.init_app(app)


from app.model import models

app.register_blueprint(root_bp)
app.register_blueprint(user_bp)
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(course_bp)
app.register_blueprint(enrollment_bp)



__all__ = ["app"]
