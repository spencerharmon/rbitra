from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class DecisionSchema(Schema):
    id = fields.UUID()
    title = fields.String()
    directory = fields.String()
    org = Relationship(
        self_view='decision_org',
        self_view_kwargs={'decision_id': '<id>'},
        related_view='org_detail',
        related_view_kwargs={'org_id': '<org.id>'}
    )
    author = Relationship(
        self_view='decision_author',
        self_view_kwargs={'decision_id': '<id>'},
        related_view='member_detail',
        related_view_kwargs={'member_id': '<author.id>'}
    )
    plugin = Relationship(
        self_view='decision_plugin',
        self_view_kwargs={'decision_id': '<id>'},
        related_view='plugin_detail',
        related_view_kwargs={'plugin_id': '<plugin.id>'}
    )
    policy = Relationship(
        self_view='decision_policy',
        self_view_kwargs={'decision_id': '<id>'},
        related_view='policy_detail',
        related_view_kwargs={'policy_id': '<policy.id>'}
    )
    approvals = Relationship(
        self_view='decision_approval',
        self_view_kwargs={'decision_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        type_='members'
    )

    class Meta:
        type_ = 'decisions'
        self_view = 'decisions_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'decisions_list'
        strict = True
