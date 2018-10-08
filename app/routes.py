from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm
from app.models import Korisnik
from app.forms import RegistrationForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/pristup', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Korisnik.query.filter_by(korisnik_login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Pogresan korisnicki nalog ili lozinka')
            return redirect(url_for('pristup'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('pristup.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Korisnik(ime=form.ime.data,prezime=form.prezime.data,adresa_ptt=form.adresa_ptt.data, adresa_mesto=form.adresa_mesto.data, adresa_ulica_broj=form.adresa_ulica_broj.data, korisnik_email=form.korisnik_email.data,id_korisnik_tip=form.id_korisnik_tip.data,  korisnik_login=form.korisnik_login.data,korisnik_pass=form.korisnik_pass.data,)
        user.set_password(form.korisnik_pass.data)
        db.session.add(user)
        db.session.commit()
        flash('Bravo, upravo ste postali registrovani korisnik!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)