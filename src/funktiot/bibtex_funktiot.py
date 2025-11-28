from pybtex.database.input import bibtex
from pybtex.database.output.bibtex import Writer
import io

def lataa_bibtex_tiedosto(bib_tiedosto):
    try:
        parser = bibtex.Parser()
        return parser.parse_file(bib_tiedosto)
    except FileNotFoundError:
        return None
    except Exception:
        return None
     
def parsi_bibtex(bib_data):
    writer = Writer()
    output = io.StringIO()
    writer.write_stream(bib_data, output)
    return output.getvalue()

def tallenna(konsoli, viiteavain, entry, bib_tiedosto, bib_data):
    # Lisää uusi viite viitteet.bib
    bib_data.entries[viiteavain] = entry
    
    otsikko = entry.fields.get('title', 'Otsikkoa ei syötetty')
    # Tallenna tiedostoon
    try:
        writer = Writer()
        with open(bib_tiedosto, 'w', encoding='utf-8') as f:
            writer.write_stream(bib_data, f)
        konsoli.kirjoita(f"lähde '{otsikko}' lisätty.\n")
    except Exception as e:
        konsoli.kirjoita(f"Virhe tallennuksessa: {e}\n")