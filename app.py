from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('config')


db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models.compte import Compte
from models.transaction import Transaction
from models.admin import Admin
from models.distributeur import Distributeur
from models.recharge import Recharge

from routes.admin_routes import admin
from routes.auth_routes import auth
from routes.client_routes import frontend
from routes.distributeur_routes import distributeur

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(distributeur, url_prefix='/distributeur')
app.register_blueprint(frontend, url_prefix='/client')

def fixture():
    admin = Admin(login='admin', nom='Dansomon ', prenom='Esse Jacques', password='admin')
    compte = Compte(nom='Minawo', telephone='123456789', admin_name=admin.nom)
    compte2 = Compte(nom='Fall', telephone='012345678', admin_name=admin.nom)
    distributeur = Distributeur(nom='Distributeur 1', prenom='Orange Money', email='distributeur@gmail.com')
    distributeur2 = Distributeur(nom='Distributeur 2', prenom='Free Sn', email='distributeur2@gmail.com')
    admin.save()
    compte.save()
    distributeur.save()
    compte2.save()
    distributeur2.save()
#fixture()
if __name__ == '__main__':
    app.run()
