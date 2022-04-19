from flask import Blueprint, request

from controllers import client_controller

frontend = Blueprint("frontend", __name__)
from app import app


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return client_controller.profile(request)


@app.route('/mes-transactions', methods=['GET', 'POST'])
def mes_transactions():
    return client_controller.mes_transactions(request)


@app.route('/mes-recharges', methods=['GET'])
def mes_recharges():
    return client_controller.mes_recharges(request)


@app.route('/recharger-account', methods=['GET', 'POST'])
def recharger_compte():
    return client_controller.recharger_compte(request)
