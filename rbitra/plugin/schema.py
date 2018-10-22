from marshmallow_jsonapi import Schema, fields


class PluginSchema(Schema):
    uuid = fields.UUID()
    title = fields.String()
    module_name = fields.String()
    path = fields.String()
