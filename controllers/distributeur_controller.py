from flask import render_template, flash, redirect, url_for

from lib import session
from models.compte import Compte
from models.recharge import Recharge


def get_profile(request):
    if request.method == 'GET' and session.is_distributeur():
        session.add_page_to_session('profile')
        return render_template('distributeur/profile.html')
    else:
        return redirect(url_for('login_all_users'))


def recharge(request):
    session.add_page_to_session('profile')
    if session.is_distributeur():
        if request.method == 'POST':
            numero = request.form['numero']
            montant = int(request.form['montant'])
            compte = Compte.query.filter_by(numero_compte=numero).first()
            if compte is not None:
                if not compte.etat:
                    flash('Compte bloque', 'error')
                    return redirect(url_for('distributeur.distributeur_profile'))
                if 50000 >= montant >= 1000:
                    recharge = Recharge(compte_id=compte.id, montant=montant)
                    recharge.save()
                    flash('Recharge effectuée avec succès', 'success')
                    return redirect(url_for('distributeur.distributeur_profile'))
                else:
                    flash('Le montant doit être compris entre 1000 et 50000', 'error')
                    return redirect(url_for('distributeur.distributeur_profile'))
            else:
                flash('Numéro de compte invalide', 'error')
                return redirect(url_for('distributeur.distributeur_profile'))
        else:
            return redirect(url_for('login_all_users'))
    return redirect(url_for('login_all_users'))


def recharges(request):
    if session.is_distributeur():
        if request.method == 'GET':
            session.add_page_to_session('recharges')
            if session.is_distributeur():
                recharges = Recharge.query.order_by(Recharge.date.desc()).all()
                return render_template('distributeur/recharge_list.html', recharges=recharges)
            else:
                return redirect(url_for('login_all_users'))
        else:
            return redirect(url_for('login_all_users'))
    return redirect(url_for('login_all_users'))


def cancel_recharge(id):
    if session.is_distributeur():
        recharge = Recharge.query.filter_by(id=id).first()
        if recharge is not None:
            if recharge.status == 'en cours':
                recharge.status = 'annuler'
                recharge.save()
                flash('Recharge annulée avec succès', 'success')
                return redirect(url_for('distributeur.distributeur_recharges'))
            else:
                flash('Recharge déjà effectuée', 'error')
                return redirect(url_for('distributeur.distributeur_recharges'))
        else:
            flash('Recharge introuvable', 'error')
            return redirect(url_for('distributeur.distributeur_recharges'))
    return redirect(url_for('login_all_users'))