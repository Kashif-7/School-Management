from flask import Blueprint, request, jsonify, Response
from app.blc.teacherBLC import TeacherBLC
from webargs.flaskparser import use_args
from webargs import fields
from app import mongo
from bson import ObjectId, json_util
import json

bp = Blueprint("teacher", __name__, url_prefix="/teachers")

# Get all teachers
@bp.route("/list", methods=["GET"])
def get_all_teachers():
    with mongo.db.client.start_session() as session:
        teachers = TeacherBLC.get_all_teachers(session=session)
    return Response(json_util.dumps(teachers), mimetype='application/json')

# Get teacher by ID
@bp.route("/detail/<id>", methods=["GET"])
def get_teacher(id):
    try:
        with mongo.db.client.start_session() as session:
            teacher = TeacherBLC.get_teacher_by_id(id, session=session)
        return Response(json_util.dumps(teacher), mimetype='application/json')
    except Exception as e:
        return Response(json_util.dumps({"error": str(e)}), mimetype='application/json', status=404)

# Create a new teacher
@bp.route("/create", methods=["POST"])
@use_args(
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.Email(required=True),
        "subject": fields.String(required=True),
        "qualification": fields.String(required=True),
        "phone": fields.String(required=False)
    },
    location="json",
)
def create_teacher(args: dict):
    try:
        with mongo.db.client.start_session() as session:
            teacher = TeacherBLC.create_teacher(args=args, session=session)
        return Response(json_util.dumps(teacher), mimetype='application/json', status=201)
    except Exception as e:
        return Response(json_util.dumps({"error": str(e)}), mimetype='application/json', status=400)


@bp.route("/update/<id>", methods=["PUT"])
@use_args(
    {
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.Email(),
        "subject": fields.String(),
        "qualification": fields.String(),
        "phone": fields.String()
    },
    location="json",
)
def update_teacher(args: dict, id):
    try:
        with mongo.db.client.start_session() as session:
            teacher = TeacherBLC.update_teacher(id, args=args, session=session)
        return Response(json_util.dumps(teacher), mimetype='application/json')
    except Exception as e:
        return Response(json_util.dumps({"error": str(e)}), mimetype='application/json', status=404)


@bp.route("/delete/<id>", methods=["DELETE"])
def delete_teacher(id):
    try:
        with mongo.db.client.start_session() as session:
            result = TeacherBLC.delete_teacher(id, session=session)
        return Response(json_util.dumps(result), mimetype='application/json')
    except Exception as e:
        return Response(json_util.dumps({"error": str(e)}), mimetype='application/json', status=404)
