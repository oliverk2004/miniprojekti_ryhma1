# Tiedosto toteuttaa robot testeissä tarvittavia komentoja
import os
from StubIO import StubIO
from pybtex.database import BibliographyData, Entry
from pybtex.database.input import bibtex
from pybtex.database.output.bibtex import Writer
from funktiot.lisaa_viite import lisaa_viite
from funktiot.bibtex_funktiot import tallenna

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
    
    