from flask import Blueprint, request

from controllers import distributeur_controller

distributeur = Blueprint("distributeur", __name__)


@distributeur.route("/profile", methods=["GET"])
def distributeur_profile():
    return distributeur_controller.get_profile(request)


@distributeur.route("/recharge", methods=["POST", "GET"])
def distributeur_recharge():
    return distributeur_controller.recharge(request)


@distributeur.route("/recharges", methods=["POST", "GET"])
def distributeur_recharges():
    return distributeur_controller.recharges(request)


@distributeur.route("/recharges/edit/<int:recharge_id>", methods=["GET"])
def cancel_recharge(recharge_id):
    return distributeur_controller.cancel_recharge(recharge_id)
