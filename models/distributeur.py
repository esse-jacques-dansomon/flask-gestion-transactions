import lib.lib
from app import db


class Distributeur(db.Model):
    __tablename__ = 'distributeur'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), nullable=False)
    etat = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False, default='distributeur')

    def __init__(self, nom, prenom, email):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.password = lib.lib.hashPassword('distributeur')

    def __repr__(self):
        return '<User %r>' % self.nom

    def serialize(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'password': self.password,
            'etat': self.etat,
            'role': self.role
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, distibuteur):
        self.nom = distibuteur.nom
        self.prenom = distibuteur.prenom
        self.email = distibuteur.email
        self.password = lib.lib.hashPassword(distibuteur.password)
        db.session.commit()

    def is_unique(email):
        return Distributeur.query.filter_by(email=email).first() is None and lib.lib.is_valid_email(email)


