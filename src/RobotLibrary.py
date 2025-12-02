# Tiedosto toteuttaa robot testeissä tarvittavia komentoja
import os
from StubIO import StubIO
from pybtex.database import BibliographyData, Entry
from pybtex.database.input import bibtex
from pybtex.database.output.bibtex import Writer
from funktiot.lisaa_viite import lisaa_viite
from funktiot.listaa_viitteet import listaa_viitteet
from funktiot.bibtex_funktiot import tallenna, lataa_bibtex_tiedosto

class RobotLibrary:

    def __init__(self):
        self.io = None
        self.test_bib_file = None

    
    def luo_testi_io(self):
        #Luodaan StubIO testausta varten.
        self.io = StubIO()
        return "IO luotu"
    

    def aseta_testi_tiedosto(self, tiedosto):
        self.test_bib_file = tiedosto
        return f"Testitiedosto luotu: {tiedosto}"
    

    def luo_tyhja_bib_tiedosto(self, tiedosto):
        # Luodaan tyhjä .bib-tiedosto
        bib_data = BibliographyData()
        tallenna(self.test_bib_file, bib_data)
        return f"Tiedosto luotu."
    

    def lisaa_viite_bib_tiedostoon(self, tyyppi, viiteavain, **kentät):
        bib_data = lataa_bibtex_tiedosto(self.test_bib_file)
        if bib_data is None: # Jos viitteitä ei vielä ole
            bib_data = BibliographyData()
        
        entry = Entry(tyyppi, fields=kentät)
        bib_data.entries[viiteavain] = entry
        tallenna(self.test_bib_file, bib_data)

        return f"Viite lisätty {viiteavain}"



    # Pitää luoda tiedosto, jossa nyt kun tarvitaan syötteet, sillä nyt voidaan lajitella syötteet aakkosjärjestyksessä
    def lajittele_syotteet(self, *syotteet):
        if not self.io:
            self.luo_testi_io()
        self.io.input = list(syotteet)


    # Metodi, jolla käyttäjälle listataan viitteet
    def call_listaa_viitteet(self):
        if not self.io:     # Jos ei olisi jostain syystä luotu vielä
            self.luo_testi_io()
        listaa_viitteet(self.test_bib_file, self.io)
        return "Viitteet listattu"
    

    # Pitää luoda jokin metodi, jolla saadaan poistettua testitiedosto aina, jotta ei ole montaa testitiedostoa
    def poista_testi_tiedosto(self):
        if self.test_bib_file:
            os.remove(self.test_bib_file)
            return f"Tiedosto poistettu."
        return "Ei tiedostoa mitä poistaa"
    

    # Tarvitaan jokin metodi, jolla pystytään varmistamaan, että output sisältää halutun tekstin roboteissa
    def tuloste_pitaisi_olla(self, teksti):
        output = "\n".join(self.io.output)
        if teksti in output:
            return True
        raise AssertionError(
            f"Virhe! \n"
            f"Tuloste on: \n{output}"
        )