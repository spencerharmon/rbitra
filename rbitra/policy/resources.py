from rbitra import db
from rbitra.policy.model import Policy
from rbitra.policy.schema import PolicySchema
from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship


class PolicyList(ResourceList):
    schema = PolicySchema
    data_layer = {'session': db.session,
                  'model': Policy}


class PolicyDetail(ResourceDetail):
    schema = PolicySchema
    data_layer = {'session': db.session,
                  'model': Policy}


class PolicyRelationship(ResourceRelationship):
    schema = PolicySchema
    data_layer = {'session': db.session,
                  'model': Policy}