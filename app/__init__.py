from flask import Flask, jsonify
from flask.json.provider import JSONProvider
from flask_cors import CORS
from app import config as CONF
from app.extension import mongo, build_db_uri
from app.api.root import bp as root_bp
from app.api.user import bp as user_bp
from app.api.student import bp as student_bp
from app.api.teacher import bp as teacher_bp
from app.api.course import bp as course_bp
from app.api.enrollment import bp as enrollment_bp
import datetime
import json
from bson import ObjectId
from webargs.flaskparser import parser


# Custom JSON provider to handle MongoDB ObjectID, datetime, and date objects
class MongoJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, default=self.default, **kwargs)
    
    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)
    
    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

app = Flask(__name__)
CORS(app)

# Use custom JSON provider
app.json = MongoJSONProvider(app)

app.config["MONGO_URI"] = build_db_uri(**CONF.DB_CREDENTIALS)
mongo.init_app(app)

app.register_blueprint(root_bp)
app.register_blueprint(user_bp)
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(course_bp)
app.register_blueprint(enrollment_bp)



__all__ = ["app"]
