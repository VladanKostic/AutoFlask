from app import app, db
from app.models import Korisnik, Vozilo

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Korisnik': Korisnik, 'Vozilo': Vozilo}

app.run()


