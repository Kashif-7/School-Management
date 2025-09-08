from flask import Blueprint, request, jsonify
from app.blc.studentBLC import StudentBLC
from webargs.flaskparser import use_args
from webargs import fields
from app.model.models import Student
from app.extension import db

bp = Blueprint("student", __name__)


@bp.route("/students/list", methods=["GET"])
def get_all_students():
    """Get all students."""
    students = StudentBLC.get_all_students()
    return jsonify([{
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
        "date_of_birth": student.date_of_birth.isoformat() if student.date_of_birth else None,
        "grade": student.grade,
        "address": student.address,
        "phone": student.phone,
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "updated_at": student.updated_at.isoformat() if student.updated_at else None
    } for student in students])


@bp.route("/students/detail/<int:id>", methods=["GET"])
def get_student(id):
    """Get a student by ID."""
    try:
        student = StudentBLC.get_student_by_id(id)
        return jsonify({
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "date_of_birth": student.date_of_birth.isoformat() if student.date_of_birth else None,
            "grade": student.grade,
            "address": student.address,
            "phone": student.phone,
            "created_at": student.created_at.isoformat() if student.created_at else None,
            "updated_at": student.updated_at.isoformat() if student.updated_at else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 404


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
    """Create a new student."""
    try:
        student = StudentBLC.create_student(args=args)
        return jsonify(student), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/students/update/<int:id>", methods=["PUT"])
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
    """Update a student's information."""
    try:
        result = StudentBLC.update_student(id, args=args)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/students/delete/<int:id>", methods=["DELETE"])
def delete_student(id):
    """Delete a student and their enrollments."""
    try:
        result = StudentBLC.delete_student(id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
