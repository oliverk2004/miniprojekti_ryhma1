import io
from pybtex.database.input import bibtex
from pybtex.database.output.bibtex import Writer
from pybtex.exceptions import PybtexError

def lataa_bibtex_tiedosto(bib_tiedosto):
    try:
        parser = bibtex.Parser()
        return parser.parse_file(bib_tiedosto)
    except FileNotFoundError:
        return None
    except PybtexError:
        return None

def onko_olemassa(bib_tiedosto, bib_data, konsoli):
    if bib_data is None:
        # Tiedostoa ei löydy tai se on virheellinen
        yrita_lukemista_pythonilla(bib_tiedosto, konsoli)
        return False
    if len(bib_data.entries) == 0:
        konsoli.kirjoita("Ei lähdeviitteitä.\n")
        return False
    return True

def yrita_lukemista_pythonilla(bib_tiedosto, konsoli):
    try:
        with open(bib_tiedosto, 'r', encoding='utf-8') as _:
            pass  # Tiedosto on olemassa
        konsoli.kirjoita("Virhe: BibTeX-tiedosto on virheellinen tai tyhjä.\n")
    except FileNotFoundError:
        konsoli.kirjoita(f"Ei lähdeviitteitä, sillä tiedostoa {bib_tiedosto} ei löytynyt.\n")

def parsi_bibtex(bib_data):
    writer = Writer()
    output = io.StringIO()
    writer.write_stream(bib_data, output)
    return output.getvalue()

def parsi_bibtex_lyhyt(bib_data):
    if not bib_data.entries:
        return "Ei lähdeviitteitä.\n"

    rivit = [""]

    for viiteavain, entry in bib_data.entries.items():
        otsikko = entry.fields.get('title', 'Otsikko puuttuu')
        vuosi = entry.fields.get('year', 'Vuosi puuttuu')

        rivi = f"[{viiteavain}] Otsikko: {otsikko}, Vuosi: {vuosi}"
        rivit.append(rivi)

    return "\n".join(rivit)

def tallenna(bib_tiedosto, bib_data):
    writer = Writer()
    with open(bib_tiedosto, 'w', encoding='utf-8') as f:
        writer.write_stream(bib_data, f)
