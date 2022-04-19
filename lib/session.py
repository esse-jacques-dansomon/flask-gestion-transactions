from flask import session


def add_user_to_session(user):
    session['user_connect'] = user


def add_page_to_session(page):
    session['page'] = page


def get_user_from_session():
    return session['user_connect']


def is_connected():
    return 'user_connect' in session


def is_admin():
    return 'user_connect' in session and session['user_connect']['role'] == 'admin'


def is_client():
    return 'user_connect' in session and session['user_connect']['role'] == 'user'


def is_distributeur():
    return 'user_connect' in session and session['user_connect']['role'] == 'distributeur'


def remove_user_from_session():
    session.pop('user_connect', None)
