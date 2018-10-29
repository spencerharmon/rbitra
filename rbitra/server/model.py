from rbitra import db


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fqdn = db.Column(db.String(128))
    port = db.Column(db.Integer, default=443)

    def __repr__(self):
        return '{}:{}'.format(self.fqdn, self.port)
