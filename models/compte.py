from app import db

from lib import lib


class Compte(db.Model):
    __tablename__ = 'compte'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    numero_compte = db.Column(db.String(20), unique=True, nullable=False)
    telephone = db.Column(db.String(255), unique=True, nullable=False)
    code_secret = db.Column(db.String(255), nullable=False)
    solde = db.Column(db.Float, nullable=False, default=0)
    etat = db.Column(db.Boolean, nullable=False, default=True)
    role = db.Column(db.String(20), nullable=False, default='user')
    admin_name = db.Column(db.String(255), nullable=False)
    transactions = db.relationship('Transaction', back_populates="compte", cascade="all, delete", passive_deletes=True)
    recharges = db.relationship('Recharge', back_populates="compte", cascade="all, delete", passive_deletes=True)

    def __init__(self, nom, telephone,  etat=True,  admin_name='', role='user', solde=0,):
        self.nom = nom
        self.telephone = telephone
        self.numero_compte = lib.generate_numero_compte()
        self.code_secret = lib.hashPassword('PASSER')
        self.solde = solde
        self.etat = etat
        self.role = role
        self.admin_name = admin_name

    def __repr__(self):
        return '<Compte %r>' % self.id

    def __str__(self):
        return '%s' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'telephone': self.telephone,
            'numero_compte': self.numero_compte,
            'code_secret': self.code_secret,
            'solde': self.solde,
            'etat': self.etat,
            'role': self.role,
            'admin_name': self.admin_name,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_unique(telephone):
        if Compte.query.filter_by(telephone=telephone).first():
            return False
        return True
