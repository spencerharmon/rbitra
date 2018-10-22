from rbitra import db
from rbitra.decision.model import Decision
from rbitra.decision.schema import DecisionSchema
from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship


class DecisionList(ResourceList):
    schema = DecisionSchema
    data_layer = {'session': db.session,
                  'model': Decision}


class DecisionDetail(ResourceDetail):
    schema = DecisionSchema
    data_layer = {'session': db.session,
                  'model': Decision}


class DecisionRelationship(ResourceRelationship):
    schema = DecisionSchema
    data_layer = {'session': db.session,
                  'model': Decision}
