from marshmallow_jsonapi import Schema, fields


class OrganizationSchema(Schema):
    uuid = fields.UUID()
    name = fields.String()
    server = fields.Integer()
