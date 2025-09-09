from flask import Blueprint, request, jsonify
from app.blc.courseBLC import CourseBLC
from webargs.flaskparser import use_args
from webargs import fields

bp = Blueprint("course", __name__, url_prefix="/courses")

@bp.route("/list", methods=["GET"])
def get_all_courses():
    try:
        courses = CourseBLC.get_all_courses()
        return jsonify([{
        "id": course.id,
        "name": course.name,
        "description": course.description,
        "credits": course.credits,
        "max_students": course.max_students,
        "teacher_id": course.teacher_id,
        "created_at": course.created_at.isoformat() if course.created_at else None,
        "updated_at": course.updated_at.isoformat() if course.updated_at else None
    } for course in courses])
    except Exception as e:
        return jsonify({"error": "No courses found"}), 404


@bp.route("/detail/<int:id>", methods=["GET"])
def get_course(id):
    try:
        course = CourseBLC.get_course_by_id(id)
        return jsonify({
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "credits": course.credits,
            "max_students": course.max_students,
            "teacher_id": course.teacher_id,
            "created_at": course.created_at.isoformat() if course.created_at else None,
            "updated_at": course.updated_at.isoformat() if course.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@bp.route("/create", methods=["POST"])
@use_args(
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "credits": fields.Integer(required=True),
        "teacher_id": fields.Integer(required=True),
        "max_students": fields.Integer(required=False)
    },
    location="json",
)
def create_course(args: dict):
    try:
        course = CourseBLC.create_course(args=args)
        return jsonify(course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/update/<int:id>", methods=["PUT"])
@use_args(
    {
        "name": fields.String(),
        "description": fields.String(),
        "credits": fields.Integer(),
        "teacher_id": fields.Integer(),
        "max_students": fields.Integer()
    },
    location="json",
)
def update_course(args: dict, id):
    try:
        course = CourseBLC.update_course(id, args=args)
        return jsonify(course)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_course(id):
    try:
        result = CourseBLC.delete_course(id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
