from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
from sqlalchemy.orm import synonym

"""
Bila je greska pri radu:
AttributeError: 'Korisnik' object has no attribute 'is_active'
Your User class is missing methods that flask-login expects. Flask-login provides a UserMixin, which you are importing but not using.
"""
class Korisnik(UserMixin,db.Model):
    id_korisnik = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(64), index=True, unique=True)
    prezime = db.Column(db.String(64), index=True, unique=True)
    adresa_ptt = db.Column(db.String(64), index=True, unique=True)
    adresa_mesto = db.Column(db.String(64), index=True, unique=True)
    adresa_ulica_broj = db.Column(db.String(64), index=True, unique=True)
    korisnik_email = db.Column(db.String(64), index=True, unique=True)
    id_korisnik_tip = db.Column(db.Integer, index=True)
    korisnik_login = db.Column(db.String(120), index=True, unique=True)
    korisnik_pass = db.Column(db.String(128))
    id=synonym('id_korisnik') # Resenje za raise NotImplementedError('No `id` attribute - override `get_id`') i primenu UserMix

    def __repr__(self):
        return '<Korisnik {}>'.format(self.korisnik_login)

    def set_password( self, password ):
        self.korisnik_pass = generate_password_hash(password)

    def check_password( self, password ):
        return check_password_hash(self.korisnik_pass, password)


class Vozilo(db.Model):
    id_vozilo = db.Column(db.Integer, primary_key=True)
    broj_sasije = db.Column(db.String(10), index=True, unique=True)
    marka = db.Column(db.String(25), index=True, unique=True)
    tip = db.Column(db.String(25), index=True, unique=True)

    def __repr__( self ):
        return '<Vozilo {}>'.format(self.broj_sasije)

class Servis(db.Model):
    id_servis = db.Column(db.Integer, primary_key=True)
    id_vozilo = db.Column(db.Integer, db.ForeignKey('vozilo.id_vozilo'))
    datum = db.Column(db.String, index=True, unique=True)
    opis_radova = db.Column(db.String(250), index=True, unique=True)
    iznos_radova = db.Column(db.Float, index=True, unique=True)
    id_vlasnik = db.Column(db.Integer, db.ForeignKey('korisnik.id_korisnik'))
    id_automehanicar = db.Column(db.Integer, db.ForeignKey('korisnik.id_korisnik'))

    def __repr__( self ):
        return '<Vozilo {}>'.format(self.broj_sasije)


@login.user_loader
def load_user(id_korisnik):
    return Korisnik.query.get(int(id_korisnik))