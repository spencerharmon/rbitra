from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from rbitra.models import MemberDigest

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(member, password):
    try:
        digest = MemberDigest.query.filter_by(member=member.id).first().digest
        return check_password_hash(digest, password)
    except:
        return False
