from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class UserSignupSchema(Schema):
    
    name = fields.Str(required=True, validate=fields.Length(min=2, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=fields.Length(min=6))
    
    @validates('password')
    def validate_password(self, value):
        
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters long')

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
