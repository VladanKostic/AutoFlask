from flask_table import Table, Col


class ResultsVoziloServis(Table):
    broj_sasije = Col('Br. sasije', show=False)
    datum = Col('Datum radova')
    opis_radova = Col('Opis radova')
    iznos_radova = Col('Iznos radova')

class ResultsMajstorServis(Table):
    ime = Col('Ime automeh.:', show=True)
    prezime = Col('Prezime automeh.:', show=True)
    broj_sasije = Col('Br. sasije', show=True)
    datum = Col('Datum radova')
    opis_radova = Col('Opis radova')
    iznos_radova = Col('Iznos radova')

