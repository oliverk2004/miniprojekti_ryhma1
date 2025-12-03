from .bibtex_funktiot import lataa_bibtex_tiedosto, onko_olemassa, parsi_bibtex_lyhyt, tallenna
from .konsoli_IO import KonsoliIO

def poista_viite(bib_tiedosto, konsoli: KonsoliIO):
    bib_data = lataa_bibtex_tiedosto(bib_tiedosto)

    if not onko_olemassa(bib_tiedosto, bib_data, konsoli):
        return

    bibtex_str = parsi_bibtex_lyhyt(bib_data)

    poistettava_viite = selvita_poistettava_viite(bibtex_str, konsoli, bib_data)
    if poistettava_viite is None:
        return

    poistettavan_otsikko = (bib_data.entries[poistettava_viite]
                            .fields.get('title', 'Tuntematon otsikko'))

    varmistus = vahvista(konsoli, poistettava_viite, poistettavan_otsikko)
    if varmistus:
        tallenna_poisto(bib_tiedosto, bib_data, poistettava_viite, konsoli)

def selvita_poistettava_viite(bibtex_str, konsoli, bib_data):
    while True:
        konsoli.kirjoita(f"\nLähdeviitteet:{bibtex_str}")
        syote = konsoli.lue("\nSyötä poistettavan lähteen viiteavain (peru) \n> ").strip()

        if syote == "peru":
            konsoli.kirjoita("Peruutaan poistaminen\n")
            return None
        if syote in bib_data.entries:
            return syote
        konsoli.kirjoita(f"Virheellinen viiteavain: {syote}\n")

def vahvista(konsoli, poistettavan_viite, poistettavan_otsikko):
    while True:
        varmistus = konsoli.lue(
            f'\nHaluatko poistaa viitteen {poistettavan_viite} {poistettavan_otsikko}?'
            ' Kirjoita "Kyllä" tai "Ei".\n> '
        ).strip().lower()
        if varmistus == "ei":
            konsoli.kirjoita("Perutaan viitteen poistaminen\n")
            return False
        if varmistus == "kyllä":
            return True
        konsoli.kirjoita(f"Syötettä: {varmistus} ei tunnistettu\n")

def tallenna_poisto(bib_tiedosto, bib_data, poistettava_viite, konsoli):
    del bib_data.entries[poistettava_viite]
    try:
        tallenna(bib_tiedosto, bib_data)
        konsoli.kirjoita("Viitteen poistaminen onnistui\n")
    except OSError as e:
        konsoli.kirjoita(f"Virhe viitteen poistamisen tallennuksessa: {e}\n")
