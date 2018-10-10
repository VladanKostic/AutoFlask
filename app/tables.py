from flask_table import Table, Col


class ResultsVoziloServis(Table):
    broj_sasije = Col('Br. sasije', show=False)
    datum = Col('Datum radova')
    opis_radova = Col('Opis radova')
    iznos_radova = Col('Iznos radova')
