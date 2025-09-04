from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class StudentCreateSchema(Schema):
    first_name = fields.Str(required=True, validate=fields.Length(min=2, max=50))
    last_name = fields.Str(required=True, validate=fields.Length(min=2, max=50))
    email = fields.Email(required=True)
    date_of_birth = fields.Date(required=True)
    grade = fields.Int(required=True)
    address = fields.Str(required=False)
    phone = fields.Str(required=False)
    
    @validates('grade')
    def validate_grade(self, value):
        if value < 1 or value > 12:
            raise ValidationError('Grade must be between 1 and 12')

class StudentUpdateSchema(Schema):
    first_name = fields.Str(validate=fields.Length(min=2, max=50))
    last_name = fields.Str(validate=fields.Length(min=2, max=50))
    email = fields.Email()
    date_of_birth = fields.Date()
    grade = fields.Int()
    address = fields.Str()
    phone = fields.Str()
    
    @validates('grade')
    def validate_grade(self, value):
        if value is not None and (value < 1 or value > 12):
            raise ValidationError('Grade must be between 1 and 12')
