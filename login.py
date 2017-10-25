from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=1, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])