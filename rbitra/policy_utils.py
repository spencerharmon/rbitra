from rbitra import db
from rbitra.models import Policy, RolePolicy, MemberRole, Role
from uuid import uuid4


def create_policy(name, org_uuid, option_dict, quorum=0.9):
    """

    :param name: String; name of policy
    :param org_uuid: String; UUID of Organization associated with policy
    :param option_dict: Dict; requisite data for adding a role to the policy. Format:
        {
            <String: role_uuid>: {
                'observe': Bool (default: True)
                'participate': Bool (default: True)
                'quorum_weight': Int (default: 1)
            }
        }
        The dict representing the options for a given role_uuid are all optional. Keys not specified will result in a
        rolepolicy with the corresponding default.
    :param quorum: Threshold over which decisions using this policy are considered to be approved, represented as a
        decimal value. See rbitra.decision_utils.DecisionUtils.check_quorum() for how the value compared with this
        threshold is calculated.
    :return: Policy
    """
    uuid = str(uuid4())
    policy = Policy(uuid=uuid, name=name, org=org_uuid, quorum=quorum)
    db.session.add(policy)
    db.session.commit()
    for role_uuid, options in option_dict.items():
        add_role_to_policy(policy.uuid, role_uuid, options)

    return policy


def add_role_to_policy(policy_uuid, role_uuid, options):
    """

    :param policy_uuid: String; UUID of policy
    :param role_uuid: String; UUID of role associated with policy
    :param options: Dict; contains options for the association between the role and policy. Format:
        {
            'observe': Bool (default: True)
            'participate': Bool (default: True)
            'quorum_weight': Int (default: 1)
        }
        All options are optional.
    :return:
    """

    rolepolicy = RolePolicy(policy=policy_uuid, role=role_uuid)
    if 'observe' in options.keys():
        rolepolicy.observe = options['observe']
    if 'participate' in options.keys():
        rolepolicy.participate = options['participate']
    if 'quorum_weight' in options.keys():
        rolepolicy.quorum_weight = options['quorum_weight']
    db.session.add(rolepolicy)
    db.session.commit()


def list_policies(member_uuid, org_uuid):
    '''
    :return: list of UUIDs representing policies with which a member is permitted to make decisions for the given
    organization.
    '''
    return [rolepolicy.policy
            for memberrole in MemberRole.query.filter_by(member=member_uuid)
            for rolepolicy in RolePolicy.query.filter_by(role=memberrole.role)
            if Role.query.filter_by(uuid=memberrole.role).first().org == org_uuid]
