from marshmallow_jsonapi import Schema, fields


class DecisionSchema(Schema):
    uuid = fields.UUID()
    title = fields.String()
    org = fields.UUID()
    author = fields.UUID()
    plugin = fields.Integer()
    directory = fields.String()
