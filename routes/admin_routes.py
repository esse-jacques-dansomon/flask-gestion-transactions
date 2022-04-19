from flask import Blueprint, request
from app import app
from controllers import admin_controller

admin = Blueprint("admin", __name__)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return admin_controller.dashboard()


@app.route("/dashboard/comptes", methods=["GET", "POST"])
def comptes():
    return admin_controller.comptes(request)


@app.route("/dashboard/comptes/edit/<int:id>", methods=["GET"])
def compte(id):
    return admin_controller.compte(id)


@app.route("/dashboard/comptes/add", methods=["GET", "POST"])
def add_compte():
    return admin_controller.add_compte(request)


@app.route("/dashboard/distributeurs", methods=["GET", "POST"])
def distributeurs():
    return admin_controller.distributeurs(request)



@app.route("/dashboard/distributeurs/edit/<int:id>", methods=["GET"])
def distributeur(id):
    return admin_controller.distributeur(id)


@app.route("/dashboard/distributeurs/add", methods=["GET", "POST"])
def add_distributeur():
    return admin_controller.add_distributeur(request)


@app.route("/dashboard/transactions", methods=["GET"])
def transactions():
    return admin_controller.transactions()


@app.route("/dashboard/admins", methods=["GET"])
def admins():
    return admin_controller.admins()



