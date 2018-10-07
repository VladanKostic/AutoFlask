from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Korisnik', validators=[DataRequired()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    remember_me = BooleanField('Zapamti')
    submit = SubmitField('Pristupi')