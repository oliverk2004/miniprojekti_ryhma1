from pybtex.database import BibliographyData, Entry
from pybtex.database.input import bibtex
from pybtex.database.output.bibtex import Writer
import io
from .konsoli_IO import KonsoliIO


def lataa_bibtex_tiedosto(bib_tiedosto):

    try:
        parser = bibtex.Parser()
        return parser.parse_file(bib_tiedosto)
    except FileNotFoundError:
        return None
    except Exception:
        return None


def tallenna_bibtex_tiedosto(bib_tiedosto, bib_data):

    writer = Writer()
    with open(bib_tiedosto, 'w', encoding='utf-8') as f:
        writer.write_stream(bib_data, f)


def listaa_viitteet(bib_tiedosto, konsoli: KonsoliIO):

    bib_data = lataa_bibtex_tiedosto(bib_tiedosto)
    
    if bib_data is None:
        # Tiedostoa ei löydy tai se on virheellinen
        try:
            with open(bib_tiedosto, 'r', encoding='utf-8') as f:
                pass  # Tiedosto on olemassa
            konsoli.kirjoita("Virhe: BibTeX-tiedosto on virheellinen tai tyhjä.\n")
        except FileNotFoundError:
            konsoli.kirjoita(f"Ei lähdeviitteitä, sillä tiedostoa {bib_tiedosto} ei löytynyt.\n")
        return
    
    if len(bib_data.entries) == 0:
        konsoli.kirjoita("Ei lähdeviitteitä.\n")
        return
    
    writer = Writer()
    output = io.StringIO()
    writer.write_stream(bib_data, output)
    bibtex_str = output.getvalue()
    
    konsoli.kirjoita(f"lähdeviitteet:\n{bibtex_str}")


def lisaa_viite(bib_tiedosto, konsoli: KonsoliIO):

    konsoli.kirjoita("lisätään uusi lähdeviite.")
    
    tyyppi = konsoli.lue("Tyyppi: ").strip().lower()
    viiteavain = konsoli.lue("Viiteavain: ").strip()
    
    # TODO: Halutaanko, että viiteavain pakko olla???
    if not viiteavain:
        konsoli.kirjoita("Virhe: Viiteavain ei voi olla tyhjä.\n")
        return
    
    # Lataa olemassa olevat viitteet viitteet.bib tiedostosta
    bib_data = lataa_bibtex_tiedosto(bib_tiedosto)
    if bib_data is None:
        # Taas tein tämän, jos ei olisi viitteet.bib tiedostoa jo luotuna
        bib_data = BibliographyData()
    
    # TODO: Varmaan halutaan, että ei voi tietenkään samalla viiteavaimella tehdä lähdeviitettä, koska lähteillä oma DOI???
    if viiteavain in bib_data.entries:
        konsoli.kirjoita(f"Virhe: Viiteavain '{viiteavain}' on jo käytössä.\n")
        return
    
    # Nuo kentät['author'] esimerkiksi pitää olla enkuksi tuon pybtexin takia, mutta ei muuta ohjelman suorittamisessa mitään.
    kentät = {}
    
    tekija = konsoli.lue("Tekijät: ").strip()
    if tekija:
        kentät['author'] = tekija
    
    otsikko = konsoli.lue("Otsikko: ").strip()
    if otsikko:
        kentät['title'] = otsikko
    
    vuosi = konsoli.lue("Vuosi: ").strip()
    if vuosi:
        kentät['year'] = vuosi
    
    konsoli.kirjoita("")
    
    # Luodaan Entry-objekti pybtexillä, joka kuvaa yhtä BibTex-viitettä
    # Pitäisi olla myös hyvä oliosuuntauneisuuden kannalta...
    entry = Entry(tyyppi, fields=kentät)
    
    # Näytä esikatselu
    temp_bib = BibliographyData(entries={viiteavain: entry})
    writer = Writer()
    output = io.StringIO()
    writer.write_stream(temp_bib, output)
    bibtex_preview = output.getvalue()
    
    # Varmistus
    tarkastaja = True
    while tarkastaja:
        konsoli.kirjoita("Syöttämäsi tiedot:")
        konsoli.kirjoita(bibtex_preview)
        
        varmistus = konsoli.lue('Haluatko tallentaa seuraavan viitteen? Kirjoita "Kyllä" tai "Ei".\n> ')
        
        if varmistus.lower() == "ei":
            konsoli.kirjoita("Tallennus peruutettu. Viitettä ei lisätty.")
            tarkastaja = False
            return
        elif varmistus.lower() == "kyllä":
            # Lisää uusi viite viitteet.bib
            bib_data.entries[viiteavain] = entry
            
            # Tallenna tiedostoon
            try:
                tallenna_bibtex_tiedosto(bib_tiedosto, bib_data)
                konsoli.kirjoita(f"lähde '{otsikko}' lisätty.\n")
            except Exception as e:
                konsoli.kirjoita(f"Virhe tallennuksessa: {e}\n")
            
            tarkastaja = False
        else:
            konsoli.kirjoita('Tuntematon komento.')

