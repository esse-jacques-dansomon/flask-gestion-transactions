from hmac import compare_digest

from flask import redirect, url_for, render_template, flash
from lib import lib, session
from models.admin import Admin
from models.compte import Compte
from models.distributeur import Distributeur


def logout():
    session.remove_user_from_session()
    return redirect(url_for('login_all_users'))


def profiles():
    if session.is_connected():
        switch = session.get_user_from_session()['role']
        if switch == 'admin':
            return redirect(url_for('dashboard'))
        elif switch == 'distributeur':
            return redirect(url_for('distributeur.distributeur_profile'))
        elif switch == 'client':
            return redirect(url_for('profile'))
    return render_template('auth/signup.html')


def login_all_users(request):
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        admin = Admin.query.filter_by(login=login).first()
        user = Compte.query.filter_by(telephone=login).first()
        distributeur = Distributeur.query.filter_by(email=login).first()
        if user == admin == distributeur is None:
            flash('Mauvais mot de passe ou login', 'error')
            return redirect(url_for('login_all_users'))
        elif (user and not user.etat) or (distributeur and not distributeur.etat):
            flash('Votre compte est bloqué', 'error')
            return redirect(url_for('login_all_users'))
        elif user:
            if lib.checkPassword(password=password, hash=user.code_secret):
                session.add_user_to_session(user=user.serialize())
                return redirect(url_for('profile'))
            else:
                flash('Mot de Passe Erroré', 'error')
        elif admin:
            if lib.checkPassword(password=password, hash=admin.password):
                session.add_user_to_session(user=admin.serialize())
                return redirect(url_for('dashboard'))
            else:
                flash('Mot de Passe Erroré', 'error')
        elif distributeur:
            if lib.checkPassword(password=password, hash=distributeur.password):
                session.add_user_to_session(user=distributeur.serialize())
                return redirect(url_for('distributeur.distributeur_profile'))
            else:
                flash('Mot de Passe Erroré', 'error')
        return redirect(url_for('login_all_users'))
    return profiles()

def edit_profile(request):
    if session.is_connected():
        if request.method == 'POST':
            old_password = request.form.get('old_password')
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            if old_password and password and password_confirm \
                    and compare_digest(password, password_confirm) \
                    and lib.check_password_hash(session.get_user_from_session()['password'],
                                                old_password):
                user = None
                switch = session.get_user_from_session()['role']
                if switch == 'admin':
                    user = Admin.query.get(session.get_user_from_session()['id'])
                elif switch == 'distributeur':
                    user = Distributeur.query.get(session.get_user_from_session()['id'])
                elif switch == 'client':
                    user = Compte.query.get(session.get_user_from_session()['id'])
                user.password = lib.hashPassword(password)
                user.save()
                session.remove_user_from_session()
                return redirect(url_for('login_all_users'))
            flash('Les mots de passe ne sont pas identiques', 'error')
            return profiles()
    return render_template('auth/signup.html')
