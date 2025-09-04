from flask import Blueprint, request, jsonify, Response
from app.blc.studentBLC import StudentBLC
from webargs.flaskparser import use_args
from webargs import fields
from app import mongo
from bson import ObjectId, json_util
import json

bp = Blueprint("student", __name__)


@bp.route("/students/list", methods=["GET"])
def get_all_students():
    with mongo.db.client.start_session() as session:
        students = StudentBLC.get_all_students(session=session)
    return Response(json_util.dumps(students), mimetype='application/json')

# Get student by ID
@bp.route("/students/detail/<id>", methods=["GET"])
def get_student(id):
    try:
        with mongo.db.client.start_session() as session:
            student = StudentBLC.get_student_by_id(id, session=session)
        return Response(json_util.dumps(student), mimetype='application/json')
    except Exception as e:
        return Response(json_util.dumps({"error": str(e)}), mimetype='application/json', status=404)

# Create a new student
@bp.route("/students/create", methods=["POST"])
@use_args(
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.Email(required=True),
        "date_of_birth": fields.Date(required=True),
        "grade": fields.Integer(required=True),
        "address": fields.String(required=False),
        "phone": fields.String(required=False)
    },
    location="json",
)
def create_student(args: dict):
    try:
        # Convert date_of_birth to string before passing to BLC
        if "date_of_birth" in args and hasattr(args["date_of_birth"], "isoformat"):
            args["date_of_birth"] = args["date_of_birth"].isoformat()
            
        with mongo.db.client.start_session() as session:
            student = StudentBLC.create_student(args=args, session=session)
        return Response(json_util.dumps(student), mimetype='application/json', status=201)
    except Exception as e:
        return Response(json_util.dumps({"error": str(e)}), mimetype='application/json', status=400)

# Update student
@bp.route("/students/update/<id>", methods=["PUT"])
@use_args(
    {
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.Email(),
        "date_of_birth": fields.Date(),
        "grade": fields.Integer(),
        "address": fields.String(),
        "phone": fields.String()
    },
    location="json",
)
def update_student(args: dict, id):
    try:
        # Convert date_of_birth to string before passing to BLC
        if "date_of_birth" in args and hasattr(args["date_of_birth"], "isoformat"):
            args["date_of_birth"] = args["date_of_birth"].isoformat()
            
        with mongo.db.client.start_session() as session:
            student = StudentBLC.update_student(id, args=args, session=session)
        return Response(json_util.dumps(student), mimetype='application/json')
    except Exception as e:
        return Response(json_util.dumps({"error": str(e)}), mimetype='application/json', status=404)

# Delete student
@bp.route("/students/delete/<id>", methods=["DELETE"])
def delete_student(id):
    try:
        with mongo.db.client.start_session() as session:
            result = StudentBLC.delete_student(id, session=session)
        return Response(json_util.dumps(result), mimetype='application/json')
    except Exception as e:
        return Response(json_util.dumps({"error": str(e)}), mimetype='application/json', status=404)
