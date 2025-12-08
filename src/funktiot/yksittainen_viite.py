from pybtex.database import BibliographyData
from .bibtex_funktiot import lataa_bibtex_tiedosto, onko_olemassa, parsi_bibtex_lyhyt, parsi_bibtex
from .konsoli_IO import KonsoliIO

def listaa_yksittainen_viite(bib_tiedosto, konsoli: KonsoliIO):
    bib_data = lataa_bibtex_tiedosto(bib_tiedosto)

    if not onko_olemassa(bib_tiedosto, bib_data, konsoli):
        return

    bibtex_str = parsi_bibtex_lyhyt(bib_data)
    selvita_viite(bib_data, bibtex_str, konsoli)

def selvita_viite(bib_data, bibtex_str, konsoli: KonsoliIO):
    while True:
        konsoli.kirjoita(f"\nLähdeviittet:{bibtex_str}")
        viiteavain = (konsoli.lue(
            "\nSyötä viitteen viiteavain, jonka haluat nähdä. (peru) \n> "
        ).strip())
        if viiteavain == "peru":
            konsoli.kirjoita("")
            return
        if viiteavain in bib_data.entries:
            yksittainen_viite_data = BibliographyData(
                entries={viiteavain: bib_data.entries[viiteavain]}
            )
            output = parsi_bibtex(yksittainen_viite_data)
            konsoli.kirjoita(f"\n{output}")
            return
        konsoli.kirjoita(f"Virheellinen viiteavain: {viiteavain}\n")
