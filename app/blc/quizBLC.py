from app.repository.quiz_repository import (
    QuizRepository, QuizQuestionRepository, QuizSubmissionRepository, QuizResultRepository, QuizGradingRepository
)


class QuizBLC:
    
    @staticmethod
    def create_quiz(quiz_data):
        """Create a new quiz"""
        quiz = QuizRepository.create_quiz(quiz_data)
        return {"quiz_id": quiz.id, "message": "Quiz created successfully"}
    
    @staticmethod
    def get_quiz_by_id(quiz_id):
        """Get quiz by ID"""
        quiz = QuizRepository.get_quiz_by_id(quiz_id)
        return quiz
    
    @staticmethod
    def get_quizzes_by_course(course_id):
        """Get all quizzes for a course"""
        quizzes = QuizRepository.get_quizzes_by_course(course_id)
        return quizzes
    
    @staticmethod
    def get_available_quizzes_for_student(student_id, course_id):
        """Get available quizzes for a student"""
        quizzes = QuizRepository.get_available_quizzes_for_student(student_id, course_id)
        return quizzes
    
    @staticmethod
    def preview_quiz_for_student(student_id, quiz_id):
        """Allow student to preview quiz questions before attempting"""
        preview = QuizRepository.get_quiz_preview_for_student(student_id, quiz_id)
        return preview
    
    @staticmethod
    def update_quiz(quiz_id, update_data):
        """Update quiz information"""
        quiz = QuizRepository.update_quiz(quiz_id, update_data)
        return {"quiz_id": quiz_id, "message": "Quiz updated successfully"}
    
    @staticmethod
    def delete_quiz(quiz_id):
        """Delete a quiz"""
        result = QuizRepository.delete_quiz(quiz_id)
        return {"quiz_id": quiz_id, "message": "Quiz deleted successfully"}


class QuizQuestionBLC:
    
    @staticmethod
    def create_question(question_data):
        """Create a new quiz question"""
        question = QuizQuestionRepository.create_question(question_data)
        return {"question_id": question.id, "message": "Question created successfully"}
    
    @staticmethod
    def add_question_to_quiz(question_data):
        """Add a question to a quiz"""
        question = QuizQuestionRepository.create_question(question_data)
        return {"question_id": question.id, "message": "Question added successfully"}
    
    @staticmethod
    def get_questions_by_quiz(quiz_id):
        """Get all questions for a quiz"""
        questions = QuizQuestionRepository.get_questions_by_quiz(quiz_id)
        return questions
    
    @staticmethod
    def get_quiz_questions(quiz_id):
        """Get all questions for a quiz (alias)"""
        questions = QuizQuestionRepository.get_questions_by_quiz(quiz_id)
        return questions
    
    @staticmethod
    def update_question(question_id, update_data):
        """Update a question"""
        question = QuizQuestionRepository.update_question(question_id, update_data)
        return {"question_id": question_id, "message": "Question updated successfully"}
    
    @staticmethod
    def delete_question(question_id):
        """Delete a question"""
        result = QuizQuestionRepository.delete_question(question_id)
        return {"question_id": question_id, "message": "Question deleted successfully"}


class QuizSubmissionBLC:
    
    @staticmethod
    def submit_quiz(student_id, submission_data):
        """Submit a quiz with answers"""
        submission_id = QuizSubmissionRepository.submit_quiz(student_id, submission_data)
        return {"submission_id": submission_id, "message": "Quiz submitted successfully"}
    
    @staticmethod
    def get_student_submissions(student_id):
        """Get all quiz submissions by a student"""
        submissions = QuizSubmissionRepository.get_student_submissions(student_id)
        return submissions
    
    @staticmethod
    def get_quiz_submissions(quiz_id):
        """Get all submissions for a quiz"""
        submissions = QuizSubmissionRepository.get_submissions_by_quiz(quiz_id)
        return submissions
    
    @staticmethod
    def get_submission_answers_details(submission_id):
        """Get detailed answers for a specific submission"""
        details = QuizSubmissionRepository.get_submission_answers_details(submission_id)
        return details


class QuizGradingBLC:
    
    @staticmethod
    def auto_grade_submission(submission_id):
        """Automatically grade a quiz submission"""
        result = QuizGradingRepository.auto_grade_submission(submission_id)
        return {"message": "Quiz graded automatically", **result}
    
    @staticmethod
    def manual_grade_submission(submission_id, teacher_feedback=None, override_marks=None):
        """Manually grade or update grading for a submission"""
        result = QuizGradingRepository.manual_grade_submission(submission_id, teacher_feedback, override_marks)
        return {"submission_id": submission_id, "message": "Quiz graded by teacher successfully"}


class QuizResultBLC:
    
    @staticmethod
    def get_quiz_results(quiz_id):
        """Get all results for a quiz"""
        results = QuizResultRepository.get_results_by_quiz(quiz_id)
        return results
    
    @staticmethod
    def get_student_results_by_course(student_id, course_id):
        """Get all quiz results for a student in a course"""
        results = QuizResultRepository.get_student_results_by_course(student_id, course_id)
        return results
    
    @staticmethod
    def get_result_by_submission(submission_id):
        """Get result by submission ID"""
        result = QuizResultRepository.get_result_by_submission(submission_id)
        return result
