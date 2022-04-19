from datetime import datetime

from app import db


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    compte = db.relationship('Compte', back_populates='transactions')

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)  # repr() is used for debugging

    def __init__(self, compte_id, type, amount, message):
        self.compte_id = compte_id
        self.type = type
        self.amount = amount
        self.message = message  # message is optional
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def serialize(self):
        return {
            'id': self.id,
            'compte_id': self.compte_id,
            'type': self.type,
            'amount': self.amount,
            'message': self.message,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = datetime.utcnow()
        db.session.commit()
