from rbitra import db
from rbitra.organization.model import Organization
from rbitra.organization.schema import OrganizationSchema
from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship


class OrganizationList(ResourceList):
    schema = OrganizationSchema
    data_layer = {'session': db.session,
                  'model': Organization}


class OrganizationDetail(ResourceDetail):
    schema = OrganizationSchema
    data_layer = {'session': db.session,
                  'model': Organization}


class OrganizationRelationship(ResourceRelationship):
    schema = OrganizationSchema
    data_layer = {'session': db.session,
                  'model': Organization}