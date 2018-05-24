from marshmallow import Schema, fields


class OrganizationSchema(Schema):
    uuid = fields.UUID()
    name = fields.String()
    server = fields.Integer()


class MemberSchema(Schema):
    uuid = fields.UUID()
    name = fields.String()
    server = fields.Integer()


class DecisionSchema(Schema):
    uuid = fields.UUID()
    title = fields.String()
    org = fields.UUID()
    author = fields.UUID()
    plugin = fields.Integer()
    directory = fields.String()


class PluginSchema(Schema):
    uuid = fields.UUID()
    title = fields.String()
    module_name = fields.String()
    class_name = fields.String()
    path = fields.String()
