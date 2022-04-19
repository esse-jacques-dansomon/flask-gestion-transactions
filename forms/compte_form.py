from wtforms import Form, validators, PasswordField, IntegerField


class CompteForm(Form):
    telephone = IntegerField('telephone', [validators.DataRequired()])
    username = PasswordField('Ancien password', [validators.DataRequired(), validators.Length(min=5, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=5, max=35),
        validators.EqualTo('confirm', message='Les mots de passe doivent etre identiques')
    ])
    confirm = PasswordField('Repeat Password')
