from flask import Blueprint, render_template, request
from app import app

# instanciation du blueprint
from app import app
from controllers import auth_controller

auth = Blueprint("auth", __name__)


@app.route("/logout")
def logout():
    return auth_controller.logout()


@app.route("/", methods=["GET", "POST"])
def login_all_users():
    return auth_controller.login_all_users(request=request)


@app.route("/profile/edit", methods=["POST", "GET"])
def edit_profiles():
    return auth_controller.edit_profile(request)



