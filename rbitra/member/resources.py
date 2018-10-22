from rbitra import db
from rbitra.member.model import Member
from rbitra.member.schema import MemberSchema
from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship


class MemberList(ResourceList):
    schema = MemberSchema
    data_layer = {'session': db.session,
                  'model': Member}


class MemberDetail(ResourceDetail):
    schema = MemberSchema
    data_layer = {'session': db.session,
                  'model': Member}


class MemberRelationship(ResourceRelationship):
    schema = MemberSchema
    data_layer = {'session': db.session,
                  'model': Member}
