from marshmallow_jsonapi import Schema, fields


class MemberSchema(Schema):
    uuid = fields.UUID()
    name = fields.String()
    server = fields.Integer()
