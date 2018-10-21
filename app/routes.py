from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm,RegistrationForm,VoziloForm,ServisForm,VlasnistvoForm,ChoiceVozilo
from app.forms import MajstorServisPretragaForm,VoziloServisPretragaForm, VozilaPregledForm
from app.models import Korisnik,Vozilo,Servis,Vlasnistvo
from app.tables import ResultsVoziloServis, ResultsMajstorServis, ResultVozila


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


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
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Korisnik(ime=form.ime.data,prezime=form.prezime.data,adresa_ptt=form.adresa_ptt.data, adresa_mesto=form.adresa_mesto.data, adresa_ulica_broj=form.adresa_ulica_broj.data, korisnik_email=form.korisnik_email.data,id_korisnik_tip=form.id_korisnik_tip.data,  korisnik_login=form.korisnik_login.data,korisnik_pass=form.korisnik_pass.data)
        user.set_password(form.korisnik_pass.data)
        db.session.add(user)
        db.session.commit()
        flash('Bravo, upravo ste postali registrovani korisnik!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/vozilo', methods=['GET', 'POST'])
def vozilo():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    results = []

    form = VoziloForm()
    if form.validate_on_submit():
        vozilo = Vozilo(broj_sasije=form.broj_sasije.data,marka=form.marka.data,tip=form.tip.data)
        db.session.add(vozilo)
        db.session.commit()
        flash('Bravo, upravo ste evidentirali vozilo!')
        return redirect(url_for('index'))
    return render_template('vozilo.html', title='Vozilo', form=form)

@app.route('/vozilapregled',methods=['GET','POST'])
def vozilapregled():
    search = VozilaPregledForm(request.form)
    if request.method == 'POST':
        return search_results_vozila(search)

    return render_template('vozilapregled.html', title='Vozila', form=search)

@app.route('/vozilapregledrezultat',methods=['GET','POST'])
def search_results_vozila(search):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    results = []

    #search_string = search.data['izbor_brsas']
    #results = db.session.execute("select id_vozilo, broj_sasije, marka, tip from vozilo where broj_sasije like ':val%';",{'val':search_string})

    trazim = '%{0}%'.format(search.data['izbor_brsas'])
    results = Vozilo.query.filter(Vozilo.broj_sasije.like(trazim))

    if not results:
        flash('Nije pronadjen rezultat')
        return redirect(url_for('vozilapregled'))
    else:
        table = ResultVozila(results)
        table.border = True
        return render_template('vozilapregledrezultat.html', table=table)

@app.route('/servis', methods=['GET', 'POST'])
def servis():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ServisForm()
    if form.validate_on_submit():
        servis = Servis(id_vozilo=form.id_vozilo.data,datum=form.datum.data,opis_radova=form.opis_radova.data, iznos_radova=form.iznos_radova.data, id_vlasnik=form.id_vlasnik.data, id_automehanicar=form.id_automehanicar.data)
        db.session.add(servis)
        db.session.commit()
        flash('Bravo, upravo ste evidentirali uradjeni servis na vozilu!')
        return redirect(url_for('index'))
    return render_template('servis.html', title='Servsi', form=form)


@app.route('/vlasnistvo', methods=['GET', 'POST'])
def vlasnistvo():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = VlasnistvoForm()
    if form.validate_on_submit():
        vlasnistvo = Vlasnistvo(id_vozilo=form.id_vozilo.data,datum_od=form.datum_od.data,datum_do=form.datum_do.data,id_vlasnik=form.id_vlasnik.data)
        db.session.add(vlasnistvo)
        db.session.commit()
        flash('Bravo, upravo ste evidentirali vlasnistvo nad vozilom!')
        return redirect(url_for('index'))
    return render_template('vlasnistvo.html', title='vlasnistvo', form=form)

@app.route('/voziloservisrezultat')
def search_results( search ):
    results = []
    search_string = search.data['izbor']

    if search.data['izbor'] != '':
        results = db.session.execute('select vozilo.broj_sasije,servis.datum,servis.opis_radova,servis.iznos_radova\
                                     from servis, vozilo\
                                     where vozilo.broj_sasije = :val\
                                     and vozilo.id_vozilo = servis.id_vozilo;',{'val':search_string})

    if not results:
        flash('Nije pronadjen rezultat')
        return redirect(url_for('voziloservis'))
    else:
        # display results
        table = ResultsVoziloServis(results)
        table.border = True
        return render_template('voziloservisrezultat.html', table=table)


@app.route('/voziloservis', methods=['GET', 'POST'])
def voziloservis():
    search = VoziloServisPretragaForm(request.form)
    if request.method == 'POST':
            return search_results(search)

    return render_template('voziloservis.html', title='Servis', form=search)


@app.route('/majstorservis', methods=['GET', 'POST'])
def majstorservis():
    search1 = MajstorServisPretragaForm(request.form)
    if request.method == 'POST':
        return search_majstorservis_results(search1)

    return render_template('majstorservis.html', title='Servis', form=search1)

@app.route('/majstorservisrezultat')
def search_majstorservis_results( search ):
    results = []
    search_string = search.data['izbor_majstor']

    if search.data['izbor_majstor'] != '':
        results = db.session.execute('select korisnik.ime,korisnik.prezime,vozilo.broj_sasije,servis.datum,servis.opis_radova,servis.iznos_radova\
                                     from korisnik, servis, vozilo\
                                     where korisnik.ime = :val\
                                     and servis.id_automehanicar = korisnik.id_korisnik\
                                     and servis.id_vozilo = vozilo.id_vozilo;',{'val':search_string})

    if not results:
        flash('Nije pronadjen rezultat!')
        return redirect(url_for('majstorservis'))
    else:
        # display results
        table1 = ResultsMajstorServis(results)
        table1.border = True
        return render_template('majstorservisrezultat.html', table=table1)

@app.route('/graf')
def graf():
    results = []
    labels = []
    values = []

    results = db.session.execute('select vozilo.broj_sasije,servis.iznos_radova\
                                  from servis,vozilo\
                                  where servis.id_vozilo = vozilo.id_vozilo\
                                  group by vozilo.broj_sasije;')

    for row in results:
      labels.append(row["broj_sasije"])
      values.append(row["iznos_radova"])

    """
    labels = [
        'AA', 'BB'
    ]

    values = [
        967.67, 1190.89, 1079.75, 1349.19,
        2328.91, 2504.28, 2873.83, 4764.87,
        4349.29, 6458.30, 9907, 16297
    ]
    """
    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


    line_labels=labels
    line_values=values
    return render_template('graf.html', title='Troskovnik vozlila', max=45000, labels=line_labels, values=line_values)
