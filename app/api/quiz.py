from flask import Blueprint, request, jsonify
from app.blc.quizBLC import QuizBLC, QuizQuestionBLC, QuizSubmissionBLC, QuizGradingBLC, QuizResultBLC
from app.schema.quiz_schema import QuizSchema, QuizQuestionSchema, QuizSubmissionSchema, QuizResultSchema, QuizSubmitSchema
from webargs.flaskparser import use_args
from webargs import fields
from datetime import datetime
from marshmallow import ValidationError

bp = Blueprint("quiz", __name__, url_prefix="/quizzes")

@bp.route("/create", methods=["POST"])
def create_quiz():
    """Create a new quiz (Teacher)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["course_id", "title", "start_date", "end_date"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400
        
        # Convert date strings to datetime
        if isinstance(data.get("start_date"), str):
            data["start_date"] = datetime.fromisoformat(data["start_date"])
        if isinstance(data.get("end_date"), str):
            data["end_date"] = datetime.fromisoformat(data["end_date"])
        
        result = QuizBLC.create_quiz(data)
        return jsonify(result), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@bp.route("/<int:quiz_id>", methods=["GET"])
def get_quiz(quiz_id):
    """Get quiz details with questions"""
    try:
        quiz = QuizBLC.get_quiz_by_id(quiz_id)
        
        quiz_data = {
            "id": quiz.id,
            "course_id": quiz.course_id,
            "course_name": quiz.course.name,
            "title": quiz.title,
            "description": quiz.description,
            "total_marks": quiz.total_marks,
            "duration_minutes": quiz.duration_minutes,
            "start_date": quiz.start_date.isoformat() if quiz.start_date else None,
            "end_date": quiz.end_date.isoformat() if quiz.end_date else None,
            "is_active": quiz.is_active,
            "created_at": quiz.created_at.isoformat() if quiz.created_at else None,
            "question_count": len(quiz.questions),
            "questions": [{
                "id": q.id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "marks": q.marks,
                "order_number": q.order_number
            } for q in sorted(quiz.questions, key=lambda x: x.order_number)]
        }
        
        return jsonify(quiz_data), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@bp.route("/course/<int:course_id>", methods=["GET"])
def get_quizzes_by_course(course_id):
    """Get all quizzes for a course (Teacher view)"""
    try:
        quizzes = QuizBLC.get_quizzes_by_course(course_id)
        
        quiz_list = [{
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "total_marks": quiz.total_marks,
            "duration_minutes": quiz.duration_minutes,
            "start_date": quiz.start_date.isoformat() if quiz.start_date else None,
            "end_date": quiz.end_date.isoformat() if quiz.end_date else None,
            "is_active": quiz.is_active,
            "created_at": quiz.created_at.isoformat() if quiz.created_at else None,
            "question_count": len(quiz.questions)
        } for quiz in quizzes]
        
        return jsonify(quiz_list), 200
        
    except Exception as e:
        return jsonify({"error": f"Error fetching quizzes: {str(e)}"}), 500


@bp.route("/<int:quiz_id>", methods=["PUT"])
def update_quiz(quiz_id):
    """Update quiz information (Teacher)"""
    try:
        data = request.get_json()
        
        # Convert date strings to datetime if provided
        if data.get("start_date") and isinstance(data.get("start_date"), str):
            data["start_date"] = datetime.fromisoformat(data["start_date"])
        if data.get("end_date") and isinstance(data.get("end_date"), str):
            data["end_date"] = datetime.fromisoformat(data["end_date"])
        
        result = QuizBLC.update_quiz(quiz_id, data)
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@bp.route("/<int:quiz_id>", methods=["DELETE"])
def delete_quiz(quiz_id):
    """Delete a quiz (Teacher)"""
    try:
        result = QuizBLC.delete_quiz(quiz_id)
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


# Quiz Question Management Endpoints

@bp.route("/<int:quiz_id>/questions", methods=["POST"])
def add_question_to_quiz(quiz_id):
    """Add a question to a quiz (Teacher)"""
    try:
        data = request.get_json()
        data["quiz_id"] = quiz_id
        
        # Validate required fields
        required_fields = ["question_text", "question_type", "correct_answer", "order_number"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400
        
        result = QuizQuestionBLC.add_question_to_quiz(data)
        return jsonify(result), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500



@bp.route("/<int:quiz_id>/questions", methods=["GET"])
def get_quiz_questions(quiz_id):
    """Get all questions for a quiz"""
    try:
        questions = QuizQuestionBLC.get_quiz_questions(quiz_id)
        
        question_list = [{
            "id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "marks": q.marks,
            "order_number": q.order_number
        } for q in questions]
        
        return jsonify(question_list), 200
        
    except Exception as e:
        return jsonify({"error": f"Error fetching questions: {str(e)}"}), 500


@bp.route("/questions/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    """Update a quiz question (Teacher)"""
    try:
        data = request.get_json()
        result = QuizQuestionBLC.update_question(question_id, data)
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@bp.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    """Delete a quiz question (Teacher)"""
    try:
        result = QuizQuestionBLC.delete_question(question_id)
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


# Student Quiz Endpoints

@bp.route("/student/<int:student_id>/course/<int:course_id>/available", methods=["GET"])
def get_available_quizzes_for_student(student_id, course_id):
    """Get available quizzes for a student in a course"""
    try:
        quizzes = QuizBLC.get_available_quizzes_for_student(student_id, course_id)
        
        quiz_list = [{
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "total_marks": quiz.total_marks,
            "duration_minutes": quiz.duration_minutes,
            "start_date": quiz.start_date.isoformat() if quiz.start_date else None,
            "end_date": quiz.end_date.isoformat() if quiz.end_date else None,
            "question_count": len(quiz.questions)
        } for quiz in quizzes]
        
        return jsonify(quiz_list), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error fetching available quizzes: {str(e)}"}), 500


@bp.route("/student/<int:student_id>/quiz/<int:quiz_id>/preview", methods=["GET"])
def preview_quiz_for_student(student_id, quiz_id):
    """Allow student to preview quiz questions before attempting"""
    try:
        quiz_preview = QuizBLC.preview_quiz_for_student(student_id, quiz_id)
        return jsonify(quiz_preview), 200
        
    except ValueError as e:
        # Handle business logic errors (enrollment, already submitted, etc.)
        if "not enrolled" in str(e):
            return jsonify({"error": str(e)}), 403
        elif "already been submitted" in str(e):
            return jsonify({"error": str(e)}), 409
        elif "not found" in str(e):
            return jsonify({"error": str(e)}), 404
        else:
            return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error fetching quiz preview: {str(e)}"}), 500


@bp.route("/student/<int:student_id>/submit/<int:quiz_id>", methods=["POST"])
def submit_quiz(student_id, quiz_id):
    try:
        raw_text = request.get_data(as_text=True)
        if not raw_text:
            raw_text = ""
        text = raw_text.strip()
        
        if not text:
            answers = []
        elif '\n' in text:
            answers = [answer.strip() for answer in text.split('\n')]
        elif ',' in text:
            answers = [answer.strip() for answer in text.split(',')]
        else:
            answers = [text.strip()]
        questions = QuizQuestionBLC.get_quiz_questions(quiz_id)
        sorted_questions = sorted(questions, key=lambda x: x.order_number)
        formatted_answers = []
        for i, question in enumerate(sorted_questions):
            answer_text = answers[i] if i < len(answers) else ""
            formatted_answers.append({
                "question_id": question.id,
                "answer": answer_text
            })
        submission_data = {
            "quiz_id": quiz_id,
            "answers": formatted_answers
        }
        
        result = QuizSubmissionBLC.submit_quiz(student_id, submission_data)
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({"error": f"Submission error: {str(e)}"}), 500

@bp.route("/<int:quiz_id>/submissions", methods=["GET"])
def get_quiz_submissions(quiz_id):
    """Get all submissions for a quiz (Teacher view)"""
    try:
        submissions = QuizSubmissionBLC.get_quiz_submissions(quiz_id)
        
        submission_list = [{
            "id": submission.id,
            "student_id": submission.student_id,
            "student_name": f"{submission.student.first_name} {submission.student.last_name}",
            "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
            "time_taken_minutes": submission.time_taken_minutes,
            "is_completed": submission.is_completed
        } for submission in submissions]
        
        return jsonify(submission_list), 200
        
    except Exception as e:
        return jsonify({"error": f"Error fetching submissions: {str(e)}"}), 500


@bp.route("/submissions/<int:submission_id>/answers", methods=["GET"])
def get_submission_answers(submission_id):
    """Get detailed answers for a specific submission (Teacher view)"""
    try:
        response_data = QuizSubmissionBLC.get_submission_answers_details(submission_id)
        return jsonify(response_data), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error fetching submission answers: {str(e)}"}), 500


@bp.route("/submissions/<int:submission_id>/grade", methods=["POST"])
def manual_grade_submission(submission_id):
    """Manually grade or update grading for a submission (Teacher)"""
    try:
        data = request.get_json()
        
        feedback = data.get("feedback")
        override_marks = data.get("override_marks")
        
        result = QuizGradingBLC.manual_grade_submission(
            submission_id, 
            teacher_feedback=feedback, 
            override_marks=override_marks
        )
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@bp.route("/<int:quiz_id>/results", methods=["GET"])
def get_quiz_results(quiz_id):
    """Get all results for a quiz (Teacher view)"""
    try:
        results = QuizResultBLC.get_quiz_results(quiz_id)
        
        result_list = [{
            "id": result.id,
            "submission_id": result.submission_id,
            "student_name": f"{result.submission.student.first_name} {result.submission.student.last_name}",
            "total_marks": result.total_marks,
            "marks_obtained": result.marks_obtained,
            "percentage": result.percentage,
            "grade": result.grade,
            "graded_by_teacher": result.graded_by_teacher,
            "created_at": result.created_at.isoformat() if result.created_at else None
        } for result in results]
        
        return jsonify(result_list), 200
        
    except Exception as e:
        return jsonify({"error": f"Error fetching results: {str(e)}"}), 500


@bp.route("/submissions/<int:submission_id>/result", methods=["GET"])
def get_submission_result(submission_id):
    """Get result for a specific submission"""
    try:
        result = QuizResultBLC.get_result_by_submission(submission_id)
        
        result_data = {
            "id": result.id,
            "submission_id": result.submission_id,
            "total_marks": result.total_marks,
            "marks_obtained": result.marks_obtained,
            "percentage": result.percentage,
            "grade": result.grade,
            "feedback": result.feedback,
            "graded_by_teacher": result.graded_by_teacher,
            "graded_at": result.graded_at.isoformat() if result.graded_at else None,
            "created_at": result.created_at.isoformat() if result.created_at else None
        }
        
        return jsonify(result_data), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@bp.route("/student/<int:student_id>/course/<int:course_id>/results", methods=["GET"])
def get_student_results_by_course(student_id, course_id):
    try:
        results = QuizResultBLC.get_student_results_by_course(student_id, course_id)
        
        result_list = [{
            "id": result.id,
            "quiz_title": result.submission.quiz.title,
            "total_marks": result.total_marks,
            "marks_obtained": result.marks_obtained,
            "percentage": result.percentage,
            "grade": result.grade,
            "feedback": result.feedback,
            "submitted_at": result.submission.submitted_at.isoformat() if result.submission.submitted_at else None,
            "graded_at": result.graded_at.isoformat() if result.graded_at else None
        } for result in results]
        
        return jsonify(result_list), 200
        
    except Exception as e:
        return jsonify({"error": f"Error fetching student results: {str(e)}"}), 500
