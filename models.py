from app import db
import datetime

class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    is_verified = db.Column(db.Boolean, default=False)
    first_sms = db.Column(db.String())
    received_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    telephone = db.Column(db.String())

    def __init__(self, first_sms, telephone):
        self.first_sms = first_sms
        self.telephone = telephone

    def __repr__(self):
        return '<id {}>'.format(self.id)
