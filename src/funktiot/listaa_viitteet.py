from pybtex.database import BibliographyData, Entry
from pybtex.database.input import bibtex
from pybtex.database.output.bibtex import Writer
import io
from .konsoli_IO import KonsoliIO
from .bibtex_funktiot import lataa_bibtex_tiedosto, parsi_bibtex

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
    
    bibtex_str = parsi_bibtex(bib_data)
    
    konsoli.kirjoita(f"lähdeviitteet:\n{bibtex_str}")