from flask import Blueprint, request, jsonify
from app.blc.enrollmentBLC import EnrollmentBLC
from webargs.flaskparser import use_args
from webargs import fields
from datetime import date

bp = Blueprint("enrollment", __name__, url_prefix="/enrollments")


@bp.route("/list", methods=["GET"])
def get_all_enrollments():
    enrollments = EnrollmentBLC.get_all_enrollments()
    return jsonify([{
        "id": enrollment.id,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id,
        "enrollment_date": enrollment.enrollment_date.isoformat() if enrollment.enrollment_date else None,
        "status": enrollment.status,
        "grade": enrollment.grade,
        "created_at": enrollment.created_at.isoformat() if enrollment.created_at else None,
        "updated_at": enrollment.updated_at.isoformat() if enrollment.updated_at else None
    } for enrollment in enrollments])


@bp.route("/by-student/<int:student_id>", methods=["GET"])
def get_student_enrollments(student_id):
    try:
        enrollments = EnrollmentBLC.get_enrollments_by_student(student_id)
        return jsonify([{
            "id": enrollment.id,
            "student_id": enrollment.student_id,
            "course_id": enrollment.course_id,
            "enrollment_date": enrollment.enrollment_date.isoformat() if enrollment.enrollment_date else None,
            "status": enrollment.status,
            "grade": enrollment.grade,
            "created_at": enrollment.created_at.isoformat() if enrollment.created_at else None,
            "updated_at": enrollment.updated_at.isoformat() if enrollment.updated_at else None
        } for enrollment in enrollments])
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/by-course/<int:course_id>", methods=["GET"])
def get_course_enrollments(course_id):
    try:
        enrollments = EnrollmentBLC.get_enrollments_by_course(course_id)
        return jsonify([{
            "id": enrollment.id,
            "student_id": enrollment.student_id,
            "course_id": enrollment.course_id,
            "enrollment_date": enrollment.enrollment_date.isoformat() if enrollment.enrollment_date else None,
            "status": enrollment.status,
            "grade": enrollment.grade,
            "created_at": enrollment.created_at.isoformat() if enrollment.created_at else None,
            "updated_at": enrollment.updated_at.isoformat() if enrollment.updated_at else None
        } for enrollment in enrollments])
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/create", methods=["POST"])
@use_args(
    {
        "student_id": fields.Integer(required=True),
        "course_id": fields.Integer(required=False),
        "course_name": fields.String(required=False),
        "enrollment_date": fields.Date(required=False)  # Optional, will default to today
    },
    location="json",
)
def create_enrollment(args: dict):
    if "course_id" not in args and "course_name" not in args:
        return jsonify({"error": "Either course_id or course_name must be provided"}), 400
        
    try:
        enrollment = EnrollmentBLC.create_enrollment(args=args)
        return jsonify(enrollment), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/update/<int:id>", methods=["PUT"])
@use_args(
    {
        "status": fields.String(required=False),
        "grade": fields.Float(required=False),
        "enrollment_date": fields.Date(required=False)
    },
    location="json",
)
def update_enrollment(args: dict, id):
    try:
        enrollment = EnrollmentBLC.update_enrollment(id, args=args)
        return jsonify(enrollment)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_enrollment(id):
    try:
        result = EnrollmentBLC.delete_enrollment(id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
