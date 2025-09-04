from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class EnrollmentCreateSchema(Schema):
    student_id = fields.Str(required=True)
    course_id = fields.Str(required=True)
    enrollment_date = fields.Str(required=True)  # Changed to Str for simplicity

class EnrollmentUpdateSchema(Schema):
    status = fields.Str(required=True)
    grade = fields.Float()
    
    @validates('status')
    def validate_status(self, value):
        valid_statuses = ['active', 'completed', 'withdrawn', 'pending']
        if value not in valid_statuses:
            raise ValidationError(f'Status must be one of: {", ".join(valid_statuses)}')
            
    @validates('grade')
    def validate_grade(self, value):
        if value is not None and (value < 0 or value > 100):
            raise ValidationError('Grade must be between 0 and 100')
