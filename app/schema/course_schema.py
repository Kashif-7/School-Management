from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class CourseCreateSchema(Schema):
    name = fields.Str(required=True, validate=fields.Length(min=2, max=100))
    description = fields.Str(required=True)
    credits = fields.Int(required=True)
    teacher_id = fields.Str(required=True)
    max_students = fields.Int(required=False)
    
    @validates('credits')
    def validate_credits(self, value):
        if value < 1 or value > 6:
            raise ValidationError('Credits must be between 1 and 6')
            
    @validates('max_students')
    def validate_max_students(self, value):
        if value is not None and (value < 1 or value > 100):
            raise ValidationError('Maximum students must be between 1 and 100')

class CourseUpdateSchema(Schema):
    name = fields.Str(validate=fields.Length(min=2, max=100))
    description = fields.Str()
    credits = fields.Int()
    teacher_id = fields.Str()
    max_students = fields.Int()
    
    @validates('credits')
    def validate_credits(self, value):
        if value is not None and (value < 1 or value > 6):
            raise ValidationError('Credits must be between 1 and 6')
            
    @validates('max_students')
    def validate_max_students(self, value):
        if value is not None and (value < 1 or value > 100):
            raise ValidationError('Maximum students must be between 1 and 100')
