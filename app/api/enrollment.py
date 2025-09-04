from flask import Blueprint, request, jsonify
from app.blc.enrollmentBLC import EnrollmentBLC
from webargs.flaskparser import use_args
from webargs import fields
from app import mongo
from bson import ObjectId

bp = Blueprint("enrollment", __name__, url_prefix="/enrollments")


@bp.route("/list", methods=["GET"])
def get_all_enrollments():
    with mongo.db.client.start_session() as session:
        enrollments = EnrollmentBLC.get_all_enrollments(session=session)
    return jsonify(enrollments)


@bp.route("/by-student/<student_id>", methods=["GET"])
def get_student_enrollments(student_id):
    try:
        with mongo.db.client.start_session() as session:
            enrollments = EnrollmentBLC.get_enrollments_by_student(student_id, session=session)
        return jsonify(enrollments)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/by-course/<course_id>", methods=["GET"])
def get_course_enrollments(course_id):
    try:
        with mongo.db.client.start_session() as session:
            enrollments = EnrollmentBLC.get_enrollments_by_course(course_id, session=session)
        return jsonify(enrollments)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/create", methods=["POST"])
@use_args(
    {
        "student_id": fields.String(required=True),
        "course_id": fields.String(required=True),
        "enrollment_date": fields.String(required=True)  # Changed to String for simplicity
    },
    location="json",
)
def create_enrollment(args: dict):
    try:
        with mongo.db.client.start_session() as session:
            enrollment = EnrollmentBLC.create_enrollment(args=args, session=session)
        return jsonify(enrollment), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/update/<id>", methods=["PUT"])
@use_args(
    {
        "status": fields.String(required=True),
        "grade": fields.Float()
    },
    location="json",
)
def update_enrollment(args: dict, id):
    try:
        with mongo.db.client.start_session() as session:
            enrollment = EnrollmentBLC.update_enrollment(id, args=args, session=session)
        return jsonify(enrollment)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/delete/<id>", methods=["DELETE"])
def delete_enrollment(id):
    try:
        with mongo.db.client.start_session() as session:
            result = EnrollmentBLC.delete_enrollment(id, session=session)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
