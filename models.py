from app import db
import datetime

class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    is_verified = db.Column(db.Boolean, default=False)
    first_sms = db.Column(db.String())
    received_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    telephone = db.Column(db.String())

    def __init__(self, telephone):
        self.telephone = telephone

    def __repr__(self):
        return '<id {}>'.format(self.id)
