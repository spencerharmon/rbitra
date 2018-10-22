from rbitra import create_app
from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

api = Api(create_app())

api.route(
    DecisionList,
    'decision_list',
    ['/decisions'])
api.route(
    DecisionDetail,
    'decision_detail',
    ['/decisions/<str:id>'])
api.route(
    DecisionRelationships,
    'decision_relationships',
    (['organizations/<str:org>/relationships/decisions'])
)
api.route(
    OrganizationList,
    'organization_list',
    ['/organizations'])
api.route(
    OrganizationDetail,
    'organization_detail',
    ['/organizations/<str:id>'])
api.route(
    MemberList,
    'member_list',
    ['/organizations/<str:org>/relationships/members'])
api.route(
    RoleList,
    'role_list',
    ['/organizations/<str:org>/roles']
)
api.route(
    RoleDetail,
    'role_detail',
    ['/organizations/<str:org>/roles/<str:id>']
)
api.route(
    RoleRelationships,
    'role_relationships',
    ['/organizations/<str:org>/relationships/roles']
)
api.route(
    PolicyList,
    'policy_list',
    ['/organizations/<str:org>/policies',
    '/policies']
)
api.route(ComputerDetail, 'computer_detail', ['/computers/<int:id>'])
api.route(ComputerRelationship, 'computer_person', ['/computers/<int:id>/relationships/owner'])