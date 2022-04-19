from datetime import datetime

from flask import render_template, redirect, url_for, flash

import lib.lib
from forms.compte_form import CompteForm
from lib import session
from lib.session import add_page_to_session
from models.compte import Compte
from models.recharge import Recharge
from models.transaction import Transaction


def profile(request):
    add_page_to_session('profile')
    if session.is_client():
        if request.method == 'GET':
            form = CompteForm(telephone=session.get_user_from_session()['telephone'])
            return render_template('client/profile.html', form=form)
        if request.method == 'POST':
            form = CompteForm(request.form)
            if form.validate():
                if not lib.lib.checkPassword(form.username.data, session.get_user_from_session()['code_secret']):
                    flash('Ancien Mot de passe incorrect', 'error')
                    return render_template('client/profile.html', form=form)
                user = Compte.query.filter_by(numero_compte=session.get_user_from_session()['numero_compte']).first()
                user.telephone = form.telephone.data
                user.code_secret = lib.lib.hashPassword(form.password.data)
                user.save()
                session.remove_user_from_session()
                return redirect(url_for('profile'))
            else:
                return render_template('client/profile.html', form=form)
    return redirect(url_for('login_all_users'))


# debit
# credit
# recharge
# debloqué ou non pour les deux
# montant valide


def mes_transactions(request):
    if session.is_client():
        add_page_to_session('Mes Transactions')
        if request.method == 'POST':

            montant = request.form['montant']
            numero_compte = request.form['numero_compte']
            if montant or numero_compte is None:
                flash('Erreur de saisie', 'error')
                return redirect(url_for('mes_transactions'))
            montant = int(montant)
            message = request.form['message']
            # return {'montant': montant, 'numero_compte': numero_compte, 'message': message}
            receiver = Compte.query.filter_by(numero_compte=numero_compte).first()
            sender = Compte.query.filter_by(numero_compte=session.get_user_from_session()['numero_compte']).first()
            if receiver is None:
                flash('Compte introuvable')
                return redirect(url_for('mes_transactions'))
            elif receiver.id == session.get_user_from_session()['id']:
                flash('Vous ne pouvez pas envoyer de l\'argent vers votre propre compte')
                return redirect(url_for('mes_transactions'))
            elif not receiver.etat:
                flash('Compte bloqué')
                return redirect(url_for('mes_transactions'))
            elif montant < 500 or montant > 5000:
                flash('Montant invi=alide doit etre entre 500 et 5000', 'error')
                return redirect(url_for('mes_transactions'))
            elif session.get_user_from_session()['solde'] - montant >= 1000:
                # print(montant, numero_compte, message)
                if not message:
                    message = 'Trasaction'
                sender_id = session.get_user_from_session()['id']
                transaction_sender = Transaction(compte_id=sender_id, amount=montant, type='debit', message=message)
                transaction_recipient = Transaction(compte_id=receiver.id, amount=montant, type='credit',
                                                    message=message)
                transaction_recipient.save()
                transaction_sender.save()
                sender.solde -= montant
                receiver.solde += montant
                sender.save()
                receiver.save()
                session.add_user_to_session(sender.serialize())
                flash('Transaction effectuée avec succès', 'success')
                return redirect(url_for('mes_transactions'))
            else:
                flash('Solde insuffisant')
                return redirect(url_for('mes_transactions'))
        else:
            add_page_to_session('Mes Transactions')
            # transactions d'un client
            transactions = Transaction.query \
                .filter_by(compte_id=session.get_user_from_session()['id']) \
                .order_by(Transaction.created_at.desc()).all()
            return render_template('client/transactions.html', transactions=transactions)
    return redirect(url_for('login_all_users'))


def recharger_compte(request):
    if request.method == 'POST':
        code = request.form['code']
        recharge = Recharge.query.filter_by(code=code).first()
        if recharge and recharge.status == 'en cours':
            montant = recharge.montant
            if montant < 1000 or montant > 50000:
                flash('Montant invalide: doit etre entre 500 et 5000', 'error')
                return redirect(url_for('recharger_compte'))
            compte = Compte.query.filter_by(numero_compte=session.get_user_from_session()['numero_compte']).first()
            transaction = Transaction(compte_id=compte.id, amount=montant, type='recharge', message='Recharge')
            transaction.save()
            compte.solde += montant
            compte.save()
            session.add_user_to_session(compte.serialize())
            flash('Rechargement effectué avec succès', 'success')
            return redirect(url_for('mes_transactions'))
        else:
            flash('Code invalide', 'error')
            return redirect(url_for('recharger_compte'))
    else:
        add_page_to_session('Profile')
        return redirect(url_for('profile'))


def mes_recharges(request):
    if session.is_client():
        add_page_to_session('Mes Recharges')
        recharges = Recharge.query \
            .filter_by(compte_id=session.get_user_from_session()['id']) \
            .order_by(Recharge.date.desc()).all()
        if recharges:
            return render_template('client/recharge_list_client.html', recharges=recharges)
        else:
            flash('Aucune recharge n\'a été trouvé', 'error')
            return render_template('client/recharge_list_client.html', recharges=recharges)
    return redirect(url_for('login_all_users'))

