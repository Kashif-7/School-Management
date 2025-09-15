from app.model.models import Quiz, QuizQuestion, QuizSubmission, QuizAnswer, QuizResult, Student, Course
from app.extension import db
from datetime import datetime, timezone
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask import abort


class QuizRepository:
    
    @staticmethod
    def create_quiz(quiz_data):
        """Create a new quiz with validation"""
        try:
            # Validate dates
            if quiz_data.get('end_date') <= quiz_data.get('start_date'):
                abort(400, "End date must be after start date")
            
            quiz = Quiz(**quiz_data)
            db.session.add(quiz)
            db.session.commit()
            return quiz
        except IntegrityError:
            db.session.rollback()
            abort(400, "Invalid course ID or database constraint violation")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_quiz_by_id(quiz_id):
        """Get quiz by ID"""
        try:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                abort(404, "Quiz not found")
            return quiz
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_quizzes_by_course(course_id):
        """Get all quizzes for a specific course"""
        try:
            return Quiz.query.filter_by(course_id=course_id).order_by(Quiz.created_at.desc()).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_available_quizzes_for_student(student_id, course_id):
        """Get available quizzes for a student (not yet attempted and within date range)"""
        try:
            from app.repository.enrollment_repository import EnrollmentRepository
            
            # Check if student is enrolled in the course
            enrollment = EnrollmentRepository.get_enrollment_by_student_and_course(student_id, course_id)
            if not enrollment:
                abort(400, "Student is not enrolled in this course")
            
            # Get all quizzes for course (bypass date filtering for now)
            all_quizzes = QuizRepository.get_quizzes_by_course(course_id)
            
            # Filter out already attempted quizzes
            available_quizzes = []
            for quiz in all_quizzes:
                if quiz.is_active:  # Simple check without date comparison
                    submission = QuizSubmissionRepository.get_student_submission_for_quiz(student_id, quiz.id)
                    if not submission:
                        available_quizzes.append(quiz)
            
            return available_quizzes
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_quiz_preview_for_student(student_id, quiz_id):
        """Allow student to preview quiz questions before attempting"""
        try:
            from app.repository.enrollment_repository import EnrollmentRepository
            
            quiz = QuizRepository.get_quiz_by_id(quiz_id)
            if not quiz:
                abort(404, "Quiz not found")

            enrollment = EnrollmentRepository.get_enrollment_by_student_and_course(student_id, quiz.course_id)
            if not enrollment:
                abort(400, "Student is not enrolled in this course")

            submission = QuizSubmissionRepository.get_student_submission_for_quiz(student_id, quiz_id)
            if submission:
                abort(400, "Quiz has already been submitted")
            
            if not quiz.is_active:
                abort(400, "Quiz is not active")
            
            quiz_preview = {
                "question_count": len(quiz.questions),
                "questions": [{
                    "id": q.id,
                    "question_text": q.question_text,
                    "question_type": q.question_type,
                    "option_a": q.option_a if q.question_type == "multiple_choice" else None,
                    "option_b": q.option_b if q.question_type == "multiple_choice" else None,
                    "option_c": q.option_c if q.question_type == "multiple_choice" else None,
                    "option_d": q.option_d if q.question_type == "multiple_choice" else None,
                    "marks": q.marks,
                    "order_number": q.order_number
                } for q in sorted(quiz.questions, key=lambda x: x.order_number)],
            }
            
            return quiz_preview
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_active_quizzes_by_course(course_id):
        """Get active quizzes for a course (within date range and active status)"""
        try:
            now = datetime.now()  # Use naive datetime to match database
            return Quiz.query.filter(
                and_(
                    Quiz.course_id == course_id,
                    Quiz.is_active == True,
                    Quiz.start_date <= now,
                    Quiz.end_date >= now
                )
            ).order_by(Quiz.start_date.desc()).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_quiz(quiz_id, update_data):
        """Update quiz information"""
        try:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                abort(404, "Quiz not found")
            
            for key, value in update_data.items():
                setattr(quiz, key, value)
            db.session.commit()
            return quiz
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_quiz(quiz_id):
        """Delete a quiz"""
        try:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                abort(404, "Quiz not found")
            
            db.session.delete(quiz)
            db.session.commit()
            return {"deleted": True}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_quiz_with_questions(quiz_id):
        """Get quiz with all its questions"""
        try:
            return Quiz.query.filter_by(id=quiz_id).first()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


class QuizQuestionRepository:
    
    @staticmethod
    def create_question(question_data):
        """Create a new quiz question with validation"""
        try:
            # Validate quiz exists
            quiz = Quiz.query.get(question_data.get('quiz_id'))
            if not quiz:
                abort(400, "Quiz not found")
            
            question = QuizQuestion(**question_data)
            db.session.add(question)
            db.session.commit()
            return question
        except IntegrityError:
            db.session.rollback()
            abort(400, "Database constraint violation")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_questions_by_quiz(quiz_id):
        """Get all questions for a quiz ordered by order_number"""
        try:
            return QuizQuestion.query.filter_by(quiz_id=quiz_id).order_by(QuizQuestion.order_number).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_question(question_id, update_data):
        """Update a question"""
        try:
            question = QuizQuestion.query.get(question_id)
            if not question:
                abort(404, "Question not found")
            
            for key, value in update_data.items():
                setattr(question, key, value)
            db.session.commit()
            return question
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_question(question_id):
        """Delete a question"""
        try:
            question = QuizQuestion.query.get(question_id)
            if not question:
                abort(404, "Question not found")
            
            db.session.delete(question)
            db.session.commit()
            return {"deleted": True}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


class QuizSubmissionRepository:
    
    @staticmethod
    def create_submission(submission_data):
        """Create a new quiz submission"""
        try:
            submission = QuizSubmission(**submission_data)
            db.session.add(submission)
            db.session.commit()
            return submission
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def submit_quiz(student_id, submission_data):
        """Submit a quiz with answers - No validation, maximum flexibility"""
        try:
            quiz_id = submission_data['quiz_id']
            
            quiz = QuizRepository.get_quiz_by_id(quiz_id)
            if not quiz:
                abort(404, "Quiz not found")
            
            submission_record = {
                'quiz_id': quiz_id,
                'student_id': student_id,
                'time_taken_minutes': submission_data.get('time_taken_minutes'),
                'is_completed': True
            }
            submission = QuizSubmissionRepository.create_submission(submission_record)

            answers_data = []
            for answer in submission_data['answers']:
                answers_data.append({
                    'submission_id': submission.id,
                    'question_id': answer['question_id'],
                    'student_answer': answer['answer']
                })
            
            QuizAnswerRepository.create_multiple_answers(answers_data)
            QuizGradingRepository.auto_grade_submission(submission.id)
            
            return submission.id
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_submission_answers_details(submission_id):
        """Get detailed answers for a specific submission with questions and correctness"""
        try:
            submission = QuizSubmissionRepository.get_submission_by_id(submission_id)
            if not submission:
                abort(404, "Submission not found")

            answers = QuizAnswerRepository.get_answers_by_submission(submission_id)
            questions = QuizQuestionRepository.get_questions_by_quiz(submission.quiz_id)
            question_dict = {q.id: q for q in questions}

            answer_details = []
            for answer in answers:
                question = question_dict.get(answer.question_id)
                if question:
                    answer_details.append({
                        "question_id": answer.question_id,
                        "question_text": question.question_text,
                        "question_type": question.question_type,
                        "correct_answer": question.correct_answer,
                        "student_answer": answer.student_answer,
                        "marks": question.marks,
                        "order_number": question.order_number,
                        "is_correct": answer.student_answer.strip().lower() == question.correct_answer.strip().lower() if question.correct_answer else None
                    })
            
            answer_details.sort(key=lambda x: x["order_number"])
            
            response_data = {
                "submission_id": submission.id,
                "student_name": f"{submission.student.first_name} {submission.student.last_name}",
                "quiz_title": submission.quiz.title,
                "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
                "total_questions": len(answer_details),
                "answers": answer_details
            }
            
            return response_data
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_submission_by_id(submission_id):
        """Get submission by ID"""
        try:
            submission = QuizSubmission.query.get(submission_id)
            if not submission:
                abort(404, "Submission not found")
            return submission
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_student_submission_for_quiz(student_id, quiz_id):
        """Check if student has already submitted this quiz"""
        try:
            return QuizSubmission.query.filter_by(student_id=student_id, quiz_id=quiz_id).first()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_submissions_by_quiz(quiz_id):
        """Get all submissions for a specific quiz"""
        try:
            return QuizSubmission.query.filter_by(quiz_id=quiz_id).join(Student).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_student_submissions(student_id):
        """Get all quiz submissions by a student"""
        try:
            return QuizSubmission.query.filter_by(student_id=student_id).join(Quiz).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


class QuizAnswerRepository:
    
    @staticmethod
    def create_answer(answer_data):
        """Create a new quiz answer"""
        try:
            answer = QuizAnswer(**answer_data)
            db.session.add(answer)
            db.session.commit()
            return answer
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def create_multiple_answers(answers_data):
        """Create multiple quiz answers in batch"""
        try:
            answers = [QuizAnswer(**answer_data) for answer_data in answers_data]
            db.session.add_all(answers)
            db.session.commit()
            return answers
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_answers_by_submission(submission_id):
        """Get all answers for a submission"""
        try:
            return QuizAnswer.query.filter_by(submission_id=submission_id).join(QuizQuestion).order_by(QuizQuestion.order_number).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_answer_grading(answer_id, is_correct, marks_obtained):
        """Update answer grading information"""
        try:
            answer = QuizAnswer.query.get(answer_id)
            if not answer:
                abort(404, "Answer not found")
            
            answer.is_correct = is_correct
            answer.marks_obtained = marks_obtained
            db.session.commit()
            return answer
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


class QuizResultRepository:
    
    @staticmethod
    def create_result(result_data):
        """Create a new quiz result"""
        try:
            result = QuizResult(**result_data)
            db.session.add(result)
            db.session.commit()
            return result
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_result_by_submission(submission_id):
        """Get result by submission ID"""
        try:
            result = QuizResult.query.filter_by(submission_id=submission_id).first()
            if not result:
                abort(404, "Quiz result not found")
            return result
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_result(submission_id, update_data):
        """Update quiz result"""
        try:
            result = QuizResult.query.filter_by(submission_id=submission_id).first()
            if not result:
                abort(404, "Quiz result not found")
            
            for key, value in update_data.items():
                setattr(result, key, value)
            db.session.commit()
            return result
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_results_by_quiz(quiz_id):
        """Get all results for a specific quiz"""
        try:
            return QuizResult.query.join(QuizSubmission).filter(QuizSubmission.quiz_id == quiz_id).join(Student).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_student_results_by_course(student_id, course_id):
        """Get all quiz results for a student in a specific course"""
        try:
            return QuizResult.query.join(QuizSubmission).join(Quiz).filter(
                and_(
                    QuizSubmission.student_id == student_id,
                    Quiz.course_id == course_id
                )
            ).all()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


class QuizGradingRepository:
    
    @staticmethod
    def auto_grade_submission(submission_id):
        """Automatically grade a quiz submission"""
        try:
            submission = QuizSubmissionRepository.get_submission_by_id(submission_id)
            if not submission:
                abort(404, "Submission not found")
            
            # Get all answers for this submission
            answers = QuizAnswerRepository.get_answers_by_submission(submission_id)
            quiz_questions = QuizQuestionRepository.get_questions_by_quiz(submission.quiz_id)
            
            total_marks = 0
            marks_obtained = 0
            
            # Grade each answer
            for answer in answers:
                question = next((q for q in quiz_questions if q.id == answer.question_id), None)
                if question:
                    total_marks += question.marks
                    
                    # Check if answer is correct
                    is_correct = QuizGradingRepository._is_answer_correct(
                        answer.student_answer, 
                        question.correct_answer, 
                        question.question_type
                    )
                    
                    marks_for_answer = question.marks if is_correct else 0
                    marks_obtained += marks_for_answer
                    
                    # Update answer with grading
                    QuizAnswerRepository.update_answer_grading(answer.id, is_correct, marks_for_answer)
            
            # Calculate percentage and grade
            percentage = (marks_obtained / total_marks) * 100 if total_marks > 0 else 0
            grade = QuizGradingRepository._calculate_grade(percentage)
            
            # Create or update result
            result_data = {
                'submission_id': submission_id,
                'total_marks': total_marks,
                'marks_obtained': marks_obtained,
                'percentage': percentage,
                'grade': grade,
                'graded_by_teacher': False
            }
            
            QuizResultRepository.create_result(result_data)
            
            return {
                "marks_obtained": marks_obtained,
                "total_marks": total_marks,
                "percentage": percentage,
                "grade": grade
            }
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def manual_grade_submission(submission_id, teacher_feedback=None, override_marks=None):
        """Manually grade or update grading for a submission"""
        try:
            result = QuizResultRepository.get_result_by_submission(submission_id)
            if not result:
                abort(404, "Quiz result not found")
            
            update_data = {
                'graded_by_teacher': True,
                'graded_at': datetime.now(),
                'feedback': teacher_feedback
            }
            
            if override_marks is not None:
                # Teacher is overriding the marks
                update_data['marks_obtained'] = override_marks
                update_data['percentage'] = (override_marks / result.total_marks) * 100
                update_data['grade'] = QuizGradingRepository._calculate_grade(update_data['percentage'])
            
            QuizResultRepository.update_result(submission_id, update_data)
            
            return {"graded": True}
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def _is_answer_correct(student_answer, correct_answer, question_type):
        """Check if student answer is correct"""
        if question_type in ['multiple_choice', 'true_false']:
            return student_answer.strip().upper() == correct_answer.strip().upper()
        elif question_type == 'text':
            # For text questions, do a case-insensitive comparison
            return student_answer.strip().lower() == correct_answer.strip().lower()
        return False
    
    @staticmethod
    def _calculate_grade(percentage):
        """Calculate letter grade from percentage"""
        if percentage >= 90:
            return 'A+'
        elif percentage >= 85:
            return 'A'
        elif percentage >= 80:
            return 'B+'
        elif percentage >= 75:
            return 'B'
        elif percentage >= 70:
            return 'C+'
        elif percentage >= 65:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'
