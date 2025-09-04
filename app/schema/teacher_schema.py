from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class TeacherCreateSchema(Schema):
    first_name = fields.Str(required=True, validate=fields.Length(min=2, max=50))
    last_name = fields.Str(required=True, validate=fields.Length(min=2, max=50))
    email = fields.Email(required=True)
    subject = fields.Str(required=True)
    qualification = fields.Str(required=True)
    phone = fields.Str(required=False)
    
    @validates('subject')
    def validate_subject(self, value):
        if len(value) < 2:
            raise ValidationError('Subject name must be at least 2 characters long')

class TeacherUpdateSchema(Schema):
    first_name = fields.Str(validate=fields.Length(min=2, max=50))
    last_name = fields.Str(validate=fields.Length(min=2, max=50))
    email = fields.Email()
    subject = fields.Str()
    qualification = fields.Str()
    phone = fields.Str()
    
    @validates('subject')
    def validate_subject(self, value):
        if value is not None and len(value) < 2:
            raise ValidationError('Subject name must be at least 2 characters long')
