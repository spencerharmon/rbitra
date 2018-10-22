from rbitra import db
from rbitra.models import Member, Configuration, MemberDigest
from rbitra.api_errors import ServerUnconfigured
from rbitra.auth import set_password_digest
from werkzeug.security import generate_password_hash
from uuid import uuid4
import json


def create_member(name, password, email):
    """
    creates a member.
    API resource is not exposed to specify server. local server is used by default.
    """
    uuid = str(uuid4())
    member = Member(uuid=uuid, name=name, email=email)

    db.session.add(member)
    db.session.commit()

    set_password_digest(member, password)
    return member


