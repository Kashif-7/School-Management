from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime


class QuizQuestionSchema(Schema):
    id = fields.Int(dump_only=True)
    quiz_id = fields.Int(required=True)
    question_text = fields.Str(required=True, validate=validate.Length(min=10, max=2000))
    question_type = fields.Str(required=True, validate=validate.OneOf(['multiple_choice', 'true_false', 'text']))
    option_a = fields.Str(allow_none=True, validate=validate.Length(max=500))
    option_b = fields.Str(allow_none=True, validate=validate.Length(max=500))
    option_c = fields.Str(allow_none=True, validate=validate.Length(max=500))
    option_d = fields.Str(allow_none=True, validate=validate.Length(max=500))
    correct_answer = fields.Str(required=True, validate=validate.Length(max=500))
    marks = fields.Float(load_default=1.0, validate=validate.Range(min=0.1, max=100))
    order_number = fields.Int(required=True, validate=validate.Range(min=1))
    created_at = fields.DateTime(dump_only=True)

    @validates('question_type')
    def validate_question_type_options(self, value):
        if value == 'multiple_choice':
            if not all([self.get('option_a'), self.get('option_b')]):
                raise ValidationError('Multiple choice questions must have at least options A and B')
        elif value == 'true_false':
            if self.get('correct_answer') not in ['True', 'False']:
                raise ValidationError('True/False questions must have "True" or "False" as correct answer')


class QuizSchema(Schema):
    id = fields.Int(dump_only=True)
    course_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=5, max=200))
    description = fields.Str(allow_none=True)
    total_marks = fields.Float(load_default=10.0, validate=validate.Range(min=1, max=1000))
    duration_minutes = fields.Int(load_default=30, validate=validate.Range(min=5, max=300))
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    is_active = fields.Bool(load_default=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    course_name = fields.Str(dump_only=True)
    questions = fields.Nested(QuizQuestionSchema, many=True, dump_only=True)
    question_count = fields.Int(dump_only=True)

    @validates('end_date')
    def validate_end_date(self, value):
        start_date = self.get('start_date')
        if start_date and value <= start_date:
            raise ValidationError('End date must be after start date')


class QuizAnswerSchema(Schema):
    id = fields.Int(dump_only=True)
    submission_id = fields.Int(required=True)
    question_id = fields.Int(required=True)
    student_answer = fields.Str(required=True, validate=validate.Length(min=1, max=2000))
    is_correct = fields.Bool(dump_only=True)
    marks_obtained = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class QuizSubmissionSchema(Schema):
    id = fields.Int(dump_only=True)
    quiz_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    submitted_at = fields.DateTime(dump_only=True)
    time_taken_minutes = fields.Int(allow_none=True, validate=validate.Range(min=1, max=1000))
    is_completed = fields.Bool(load_default=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Nested fields
    quiz_title = fields.Str(dump_only=True)
    student_name = fields.Str(dump_only=True)
    answers = fields.Nested(QuizAnswerSchema, many=True, dump_only=True)


class QuizResultSchema(Schema):
    id = fields.Int(dump_only=True)
    submission_id = fields.Int(required=True)
    total_marks = fields.Float(required=True, validate=validate.Range(min=1))
    marks_obtained = fields.Float(required=True, validate=validate.Range(min=0))
    percentage = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    grade = fields.Str(allow_none=True, validate=validate.OneOf(['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']))
    feedback = fields.Str(allow_none=True)
    graded_by_teacher = fields.Bool(load_default=False)
    graded_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    quiz_title = fields.Str(dump_only=True)
    student_name = fields.Str(dump_only=True)


class QuizSubmitSchema(Schema):
    quiz_id = fields.Int(required=True)
    time_taken_minutes = fields.Int(allow_none=True, validate=validate.Range(min=1, max=1000))
    answers = fields.List(fields.Dict(keys=fields.Str(), values=fields.Raw()), required=True)
    
