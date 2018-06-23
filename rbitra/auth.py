from rbitra import db
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from rbitra.models import Member, MemberDigest

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    try:
        member = Member.query.filter_by(email=email).first()
        digest = MemberDigest.query.filter_by(member=member.uuid).first().digest
        return check_password_hash(digest, password)
    except:
        raise
        return False


def set_password_digest(member, password):
    """
    sets the password for the specified member to the specified string and stores the digest in the db.
    :param member: sqlalchemy db model object for member
    :param password: plaintext string
    :return: None
    """
    digest = generate_password_hash(password)
    member_digest = MemberDigest(member=member.uuid, digest=digest)
    db.session.add(member_digest)
    db.session.commit()