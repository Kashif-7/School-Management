from flask import Blueprint, request, jsonify
from app.blc.courseBLC import CourseBLC
from webargs.flaskparser import use_args
from webargs import fields
from app import mongo
from bson import ObjectId

bp = Blueprint("course", __name__, url_prefix="/courses")

@bp.route("/list", methods=["GET"])
def get_all_courses():
    with mongo.db.client.start_session() as session:
        courses = CourseBLC.get_all_courses(session=session)
    return jsonify(courses)


@bp.route("/detail/<id>", methods=["GET"])
def get_course(id):
    try:
        with mongo.db.client.start_session() as session:
            course = CourseBLC.get_course_by_id(id, session=session)
        return jsonify(course)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@bp.route("/create", methods=["POST"])
@use_args(
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "credits": fields.Integer(required=True),
        "teacher_id": fields.String(required=True),
        "max_students": fields.Integer(required=False)
    },
    location="json",
)
def create_course(args: dict):
    try:
        with mongo.db.client.start_session() as session:
            course = CourseBLC.create_course(args=args, session=session)
        return jsonify(course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/update/<id>", methods=["PUT"])
@use_args(
    {
        "name": fields.String(),
        "description": fields.String(),
        "credits": fields.Integer(),
        "teacher_id": fields.String(),
        "max_students": fields.Integer()
    },
    location="json",
)
def update_course(args: dict, id):
    try:
        with mongo.db.client.start_session() as session:
            course = CourseBLC.update_course(id, args=args, session=session)
        return jsonify(course)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/delete/<id>", methods=["DELETE"])
def delete_course(id):
    try:
        with mongo.db.client.start_session() as session:
            result = CourseBLC.delete_course(id, session=session)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
