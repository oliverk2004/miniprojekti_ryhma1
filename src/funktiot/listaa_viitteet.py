from .konsoli_IO import KonsoliIO
from .bibtex_funktiot import lataa_bibtex_tiedosto, parsi_bibtex, yrita_lukemista_pythonilla

def listaa_viitteet(bib_tiedosto, konsoli: KonsoliIO):
    bib_data = lataa_bibtex_tiedosto(bib_tiedosto)
    
    if bib_data is None:
        # Tiedostoa ei löydy tai se on virheellinen
        yrita_lukemista_pythonilla(bib_tiedosto, konsoli)
        return
    
    if len(bib_data.entries) == 0:
        konsoli.kirjoita("Ei lähdeviitteitä.\n")
        return
    
    bibtex_str = parsi_bibtex(bib_data)
    
    konsoli.kirjoita(f"lähdeviitteet:\n{bibtex_str}")