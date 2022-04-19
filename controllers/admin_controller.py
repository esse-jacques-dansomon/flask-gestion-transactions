import datetime

from flask import render_template, redirect, url_for, flash

from lib import session, lib
from lib.session import add_page_to_session
from models.admin import Admin
from models.compte import Compte
from models.distributeur import Distributeur
from models.transaction import Transaction
from sqlalchemy import func
from datetime import date
from secrets import compare_digest


def dashboard():
    if session.is_admin():
        add_page_to_session('dashboard')
        transactions_of_day = Transaction.query.filter_by(created_at=datetime.date.today()).all()
        comptes = Compte.query.all()
        comptes_bloques = Compte.query.filter_by(etat=False).all()
        admins = Admin.query.all()
        return render_template('admin/dashboard.html',
                               transactions_of_day=len(transactions_of_day),
                               comptes=len(comptes),
                               comptes_bloques=len(comptes_bloques),
                               admins=len(admins))
    return redirect(url_for('login_all_users'))


def comptes(request):
    if session.is_admin():
        add_page_to_session('comptes')
        if request.method == 'POST':
            numero = request.form.get('numero')
            etat = request.form.get('etat_compte')
            if numero is not None:
                compte = Compte.query.filter_by(numero_compte=numero.strip()).all()
                if compte:
                    return render_template('admin/comptes.html', comptes=compte)
            elif etat:
                if etat == "all":
                    return render_template('admin/comptes.html', comptes=Compte.query.all())
                etat = True if etat == 'active' else False
                comptes = Compte.query.filter_by(etat=etat).all()
                if comptes:
                    return render_template('admin/comptes.html', comptes=comptes)
            flash('Désolé, Pas de compte trouvé pour ce filtre', 'info')
            return redirect(url_for('comptes'))
        comptes = Compte.query.all()
        return render_template('admin/comptes.html', comptes=comptes)
    return redirect(url_for('login_all_users'))


def compte(id):
    if session.is_admin():
        add_page_to_session("comptes")
        compte = Compte.query.get(id)
        if compte:
            compte.etat = not compte.etat
            compte.save()
            flash(f'Compte {compte.nom} modifié avec success ', 'success')
        return redirect(url_for('comptes'))
    return redirect(url_for('login_all_users'))


def add_compte(request):
    if session.is_admin():
        add_page_to_session("dashboard")
        if request.method == 'POST':
            nom = request.form.get('nom')
            telephone = request.form.get('telephone')
            if nom and Compte.is_unique(telephone=telephone):
                compte = Compte(nom=nom, telephone=telephone)
                compte.save()
                flash(f'Compte {compte.nom} ajouté avec success ', 'success')
            return redirect(url_for('comptes'))
        elif request.method == 'GET':
            return redirect(url_for('dashboard'))
    return redirect(url_for('login_all_users'))


def transactions():
    if session.is_admin():
        add_page_to_session("transactions")
        transactions = Transaction.query.filter().all()
        return render_template('admin/transactions.html', transactions=transactions)
    return redirect(url_for('login_all_users'))


def admins():
    if session.is_admin():
        add_page_to_session("admins")
        admins = Admin.query.all()
        return render_template('admin/admins.html', admins=admins)
    return redirect(url_for('login_all_users'))

def distributeurs(request):
    if session.is_admin():
        add_page_to_session('ditributeurs')
        if request.method == 'POST':
            email = request.form.get('email')
            etat = request.form.get('etat')
            if email is not None:
                distributeur = Distributeur.query.filter_by(email=email.strip()).all()
                if distributeur:
                    return render_template('admin/distributeurs.html', distributeurs=distributeur)
                flash(f'Aucun distributeur trouvé avec l\'email {email}', 'error')
            elif etat:
                if etat == "all":
                    return render_template('admin/distributeurs.html', distributeurs=Distributeur.query.all())
                etat = True if etat == 'active' else False
                distributeurs = Distributeur.query.filter_by(etat=etat).all()
                if distributeurs:
                    return render_template('admin/distributeurs.html', distributeurs=distributeurs)
                flash('Désolé, Pas de distributeurs trouvé pour ce filtre', 'info')
            return redirect(url_for('distributeurs'))
        else:
            add_page_to_session("distributeurs")
            distributeurs = Distributeur.query.all()
            return render_template('admin/distributeurs.html', distributeurs=distributeurs)
    return redirect(url_for('login_all_users'))


def distributeur(id):
    if session.is_admin():
        add_page_to_session("distributeurs")
        distributeur = Distributeur.query.get(id)
        if compte:
            distributeur.etat = not distributeur.etat
            distributeur.save()
            flash(f'Distributeur {distributeur.nom} modifié avec success ', 'success')
        return redirect(url_for('distributeurs'))
    return redirect(url_for('login_all_users'))


def add_distributeur(request):
    if session.is_admin():
        add_page_to_session("dashboard")
        if request.method == 'POST':
            nom = request.form.get('nom')
            prenom = request.form.get('prenom')
            email = request.form.get('email')
            if nom and prenom and email :
                if Distributeur.is_unique(email=email):
                    distributeur = Distributeur(nom=nom, prenom=prenom, email=email)
                    distributeur.save()
                    flash(f'Compte {distributeur.nom} ajouté avec success ', 'success')
                    return redirect(url_for('distributeurs'))
                flash('Désolé, ce compte existe déjà', 'error')
                return redirect(url_for('dashboard'))
            flash('Veuillez remplir le formulaire svp', 'error')
            return redirect(url_for('dashboard'))
        elif request.method == 'GET':
            return redirect(url_for('dashboard'))
    return redirect(url_for('login_all_users'))