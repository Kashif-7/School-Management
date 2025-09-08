from flask import Blueprint, request, jsonify
from app.blc.teacherBLC import TeacherBLC
from webargs.flaskparser import use_args
from webargs import fields

bp = Blueprint("teacher", __name__, url_prefix="/teachers")

@bp.route("/list", methods=["GET"])
def get_all_teachers():
    teachers = TeacherBLC.get_all_teachers()
    return jsonify([{
        "id": teacher.id,
        "first_name": teacher.first_name,
        "last_name": teacher.last_name,
        "email": teacher.email,
        "subject": teacher.subject,
        "qualification": teacher.qualification,
        "phone": teacher.phone,
        "created_at": teacher.created_at.isoformat() if teacher.created_at else None,
        "updated_at": teacher.updated_at.isoformat() if teacher.updated_at else None
    } for teacher in teachers])


@bp.route("/detail/<int:id>", methods=["GET"])
def get_teacher(id):
    try:
        teacher = TeacherBLC.get_teacher_by_id(id)
        return jsonify({
            "id": teacher.id,
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "email": teacher.email,
            "subject": teacher.subject,
            "qualification": teacher.qualification,
            "phone": teacher.phone,
            "created_at": teacher.created_at.isoformat() if teacher.created_at else None,
            "updated_at": teacher.updated_at.isoformat() if teacher.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 404

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
        teacher = TeacherBLC.create_teacher(args=args)
        return jsonify(teacher), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/update/<int:id>", methods=["PUT"])
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
        teacher = TeacherBLC.update_teacher(id, args=args)
        return jsonify(teacher)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_teacher(id):
    try:
        result = TeacherBLC.delete_teacher(id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
