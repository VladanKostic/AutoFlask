from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Korisnik

class LoginForm(FlaskForm):
    username = StringField('Korisnik', validators=[DataRequired()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    remember_me = BooleanField('Zapamti')
    submit = SubmitField('Pristupi')

class RegistrationForm(FlaskForm):
    ime = StringField('Ime', validators=[DataRequired()])
    prezime = StringField('Prezime', validators=[DataRequired()])
    adresa_ptt = StringField('PTT', validators=[DataRequired()])
    adresa_mesto = StringField('Mesto', validators=[DataRequired()])
    adresa_ulica_broj = StringField('Ulica i broj', validators=[DataRequired()])
    korisnik_email = StringField('Email korisnika', validators=[DataRequired()])
    id_korisnik_tip = SelectField('Tip korisnika', choices=[('1', 'Vlasnik'),('2', 'Automehanicar')], validators=[DataRequired()])
    korisnik_login = StringField('Korisnicki nalog', validators=[DataRequired()])
    korisnik_pass = PasswordField('Lozinka', validators=[DataRequired()])
    korisnik_pass2 = PasswordField('Ponovi lozinku', validators=[DataRequired(), EqualTo('korisnik_pass')])
    submit = SubmitField('Registruj se')

    def validate_username(self, korisnik_login):
        user = Korisnik.query.filter_by(korisnik_login=korisnik_login.data).first()
        if user is not None:
            raise ValidationError('Molimo Vas da koristite drugi korisnicki nlaog.')

    def validate_email( self, korisnik_email ):
        user = Korisnik.query.filter_by(korisnik_email=korisnik_email.data).first()
        if user is not None:
            raise ValidationError('Molimo Vas da koristite razlicite email adrese.')

class VoziloForm(FlaskForm):
    broj_sasije = StringField('Broj sasije', validators=[DataRequired()])
    marka = StringField('Marka', validators=[DataRequired()])
    tip = StringField('Tip', validators=[DataRequired()])
    submit = SubmitField('Evidentiraj')

class ServisForm(FlaskForm):
    id_vozilo = StringField('Vozilo', validators=[DataRequired()])
    datum = StringField('Datum servisa', validators=[DataRequired()])
    opis_radova = StringField('Opis radova', validators=[DataRequired()])
    iznos_radova = StringField('Iznos radova', validators=[DataRequired()])
    id_vlasnik = StringField('Id vlasnika', validators=[DataRequired()])
    id_automehanicar = StringField('Id automehanicara', validators=[DataRequired()])
    submit = SubmitField('Evidentiraj')

class VoziloServisPretragaForm(FlaskForm):
    izbor = StringField('Unesi broj sasije vozila', validators=[DataRequired()])
    submit = SubmitField('Prikazi')
