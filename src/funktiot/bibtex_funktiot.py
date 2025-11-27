from .konsoli_IO import KonsoliIO
from pybtex.database import BibliographyData, Entry
from pybtex.database.input import bibtex


# Lataa ja parsee BibTex tiedoston käyttäen pybtex-kirjastoa.
def lataa_bibtex_tiedosto(bib_tiedosto):
    # tavoite, että palauttaa parsetun lähdeviitteen (siihen käytetään BibliographyData)
    try:
        parser = bibtex.Parser()
        return parser.parse_file(bib_tiedosto)
    except FileNotFoundError:
        return None
    except Exception:
        return None


def listaa_viitteet(bib_tiedosto, io: KonsoliIO):
    try:
        with open(bib_tiedosto, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            io.kirjoita("Ei lähdeviitteitä.\n")
            return
        
        io.kirjoita(f"lähdeviitteet:\n{content}\n")
    except FileNotFoundError:
        io.kirjoita(f"Ei lähdeviitteitä, sillä tiedostoa {bib_tiedosto} ei löytynyt.\n")

def lisaa_viite(bib_tiedosto, io: KonsoliIO):
    io.kirjoita("lisätään uusi lähdeviite.")
    tyyppi = io.lue("Tyyppi: ")
    viiteavain = io.lue("Viiteavain: ")
    tekijä = io.lue("Tekijät: ").strip()
    otsikko = io.lue("Otsikko: ").strip()
    vuosi = io.lue("Vuosi: ")
    io.kirjoita("")
#tähän muut tärkeät tiedot jos esim doi tarvitsee tai muuta

    bibtex_block = f"@{tyyppi}{{{viiteavain},\n" \
               f"tekijä = {{{tekijä}}},\n" \
               f"otsikko = {{{otsikko}}},\n" \
               f"vuosi = {{{vuosi}}},\n" \
               f"}}"
    
    # Tarkastetaan haluaako käyttäjä tallettaa viitteen vai peruuttaa tallennuksen.
    tarkastaja = True
    while tarkastaja == True:

        io.kirjoita('-' * 20)
        io.kirjoita("Syöttämäsi tiedot:")
        io.kirjoita(f'{bibtex_block}')

        # Käyttäjä syöttää komennon, jolla tallenetaan viite tai peruutetaan tallennus.
        varmistus = io.lue('Haluatko tallentaa seuraavan viitteen? Kirjoita "Kyllä" tai "Ei".\n> ')

        # Ei tallenneta.
        if varmistus.lower() == "ei":
            io.kirjoita("Tallennus peruutettu. Viitettä ei lisätty.")
            tarkastaja = False
            return # return-komento poistuu funktiosta

        # Tallennetaan viite.
        elif varmistus.lower() == "kyllä":
            #pitäisi luoda bibtexiin viitteen oikean muotoisena
            io.kirjoita('-' * 20)
            with open(bib_tiedosto, "a", encoding="utf-8") as f:
                f.write("\n\n" + bibtex_block)

            io.kirjoita(f"lähde '{otsikko}' lisätty.\n")
            tarkastaja = False

        # Käyttäjä syötti jotain muuta kuin hyväksytyn "kyllä" tai "ei" komennon.
        else:
            io.kirjoita('Tuntematon komento. Kirjoita "Kyllä" tai "Ei" ilman tyhjiä välejä.')