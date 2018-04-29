from rbitra import db
from rbitra.models import Member, Configuration, MemberDigest
from rbitra.api_errors import DefaultServerUnconfigured
from rbitra.auth import auth
from werkzeug.security import generate_password_hash


def create_member(name, password, srv=None):
    """
    creates a member.
    API resource is not exposed to specify server. local server is used by default.
    """
    if srv is None:
        try:
            qry = Configuration.query.filter_by(name='current_config').first()
            localsrv = qry.server
        except AttributeError as e:
            raise DefaultServerUnconfigured from e
        member = Member(name=name, server=localsrv)

        db.session.add(member)
        db.session.commit()

        set_password_digest(member, password)
    else:
        member = Member(name=name, server=srv)
        db.session.add(member)
        db.session.commit()


def set_password_digest(member, password):
    """
    sets the password for the specified member to the specified string and stores the digest in the db.
    :param member: sqlalchemy db model object for member
    :param password: plaintext string
    :return: None
    """
    digest = generate_password_hash(password)
    member_digest = MemberDigest(member=member.id, digest=digest)
    db.session.add(member_digest)
    db.session.commit()
