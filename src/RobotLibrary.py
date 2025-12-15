# Tiedosto toteuttaa robot testeissä tarvittavia komentoja
import os
from StubIO import StubIO
from pybtex.database import BibliographyData, Entry
from pybtex.database.input import bibtex
from pybtex.database.output.bibtex import Writer
from funktiot.lisaa_viite import lisaa_viite
from funktiot.poista_viite import poista_viite
from funktiot.yksittainen_viite import listaa_yksittainen_viite
from funktiot.listaa_viitteet import listaa_viitteet
from funktiot.bibtex_funktiot import tallenna, lataa_bibtex_tiedosto

class RobotLibrary:

    def __init__(self):
        self.io = None
        self.test_bib_file = None

    # Robot testejä varten...
    def luo_testi_io(self):
        #Luodaan StubIO testausta varten.
        self.io = StubIO()
        return "IO luotu"

    # Robot testejä varten...
    def aseta_testi_tiedosto(self, tiedosto):
        self.test_bib_file = tiedosto
        return f"Testitiedosto luotu: {tiedosto}"

    # Robot testejä varten...
    def luo_tyhja_bib_tiedosto(self, tiedosto):
        # Luodaan tyhjä .bib-tiedosto
        bib_data = BibliographyData()
        tallenna(self.test_bib_file, bib_data)
        return f"Tiedosto luotu."

    # Pitää luoda tiedosto, jossa nyt kun tarvitaan syötteet, sillä nyt voidaan lajitella syötteet 
    # aakkosjärjestyksessä ja vanhimmasta uusimpaan.
    def aseta_syotteet(self, *syotteet):
        if not self.io:
            self.luo_testi_io()
        self.io.input = list(syotteet)

    # Metodi, jolla käyttäjälle listataan viitteet
    def call_listaa_viitteet(self):
        if not self.io:     # Jos ei olisi jostain syystä luotu vielä
            self.luo_testi_io()
        listaa_viitteet(self.test_bib_file, self.io)
        return "Viitteet listattu"
    

    # Metodi, jolla käyttäjä lisää viitteen
    def call_lisaa_viite(self):
        if not self.io:     # Jos ei olisi jostain syystä luotu vielä
            self.luo_testi_io()
        if not self.test_bib_file:
            raise ValueError("Testitiedostoa ei ole asetettu.")
        
        lisaa_viite(self.test_bib_file, self.io)
        return "Lisää viite suoritettu"


    # Metodi, jolla käyttäjä poistaa viitteen
    def call_poista_viitteet(self):
        poista_viite(self.test_bib_file, self.io)


    # Tähän pitäisi lisätä call_hae_viite(self):
    def call_hae_viite(self):
        if not self.io:     # Jos ei olisi jostain syystä luotu vielä
            self.luo_testi_io()
        if not self.test_bib_file:
            raise ValueError("Testitiedostoa ei ole asetettu.")

        listaa_yksittainen_viite(self.test_bib_file, self.io)
        return "Viite haettu"


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
