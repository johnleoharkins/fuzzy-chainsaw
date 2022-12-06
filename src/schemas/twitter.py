

from marshmallow import Schema, fields

class TwitterAuthCallbackSchema(Schema):
    code = fields.Str()
    state = fields.Str()