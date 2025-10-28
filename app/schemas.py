from marshmallow import fields, validate, validates, ValidationError
from .extensions import ma

class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class RegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    name = fields.Str(allow_none=True)

class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class ItemSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    sku = fields.Str(required=True, validate=validate.Length(min=2, max=64))
    title = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates("price")
    def validate_price(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Price must be non-negative.")

    @validates("quantity")
    def validate_quantity(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Quantity must be non-negative.")
