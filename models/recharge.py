import uuid

import lib.lib
from app import db


# en cours
# annuler
# utilise

class Recharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    montant = db.Column(db.Integer)
    code = db.Column(db.String(255), unique=True, nullable=False, default=uuid.uuid1())
    status = db.Column(db.String(10), default='en cours')
    date = db.Column(db.DateTime, default=db.func.now())
    compte = db.relationship('Compte', back_populates='recharges')
    updated_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, compte_id, montant):
        self.compte_id = compte_id
        self.montant = montant
        self.code = lib.lib.generate_code_recharge()

    def __repr__(self):
        return '<Recharge %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'compte_id': self.compte_id,
            'montant': self.montant,
            'status': self.status,
            'date': self.date,
            'code': self.code,
            'updated_at': self.updated_at

        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
