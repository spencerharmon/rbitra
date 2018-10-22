from rbitra import db
from rbitra.role.model import Role
from rbitra.role.schema import RoleSchema
from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship


class RoleList(ResourceList):
    schema = RoleSchema
    data_layer = {'session': db.session,
                  'model': Role}


class RoleDetail(ResourceDetail):
    schema = RoleSchema
    data_layer = {'session': db.session,
                  'model': Role}


class RoleRelationship(ResourceRelationship):
    schema = RoleSchema
    data_layer = {'session': db.session,
                  'model': Role}