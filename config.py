import os

SECRET_KEY = os.urandom(32)
# Indique le dossier dans lequel script s’exécute
basedir = os.path.abspath(os.path.dirname(__file__))

# Activer le mode debug
FLASK_DEBUG = 1

# Connexion à la base de données
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db/data.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False
