from app import db
from werkzeug.security import generate_password_hash

from lib import lib


def hash_password(password):
    return generate_password_hash(password)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(80), nullable=False)
    nom = db.Column(db.String(80), nullable=False)
    login = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='admin')

    def __init__(self, prenom, nom, login, password):
        self.prenom = prenom
        self.nom = nom
        self.login = login
        self.password = hash_password(password)

    def __repr__(self):
        return f"Admin : {self.id} - {self.prenom} {self.nom} - {self.login} - {self.password} - {self.role}"

    def serialize(self):
        return {
            'id': self.id,
            'prenom': self.prenom,
            'nom': self.nom,
            'login': self.login,
            'password': self.password,
            'role': self.role
        }

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def update(self, admin):
        self.prenom = admin.prenom
        self.nom = admin.nom
        self.login = admin.login
        self.password = lib.lib.hash_password(admin.password)
        db.session.commit()
