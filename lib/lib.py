import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError


def generate_numero_compte():
    return datetime.datetime.now().strftime('%Y%d%m%H%M%S%f')


def generate_code_recharge():
    return datetime.datetime.now().strftime('%Y-%d%m-%H%M-%S-%f')


def hashPassword(password):
    return generate_password_hash(password)


def checkPassword(password, hash):
    return check_password_hash(hash, password)


def is_number(number):
    return number.isdigit()


def is_valid_email(email):
    return validate_email(email)
