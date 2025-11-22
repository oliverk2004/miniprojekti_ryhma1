from .konsoli_IO import KonsoliIO

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

#tähän muut tärkeät tiedot jos esim doi tarvitsee tai muuta
    
    bibtex_block = f"@{tyyppi}{{{viiteavain},\n" \
               f"tekijä = {{{tekijä}}},\n" \
               f"otsikko = {{{otsikko}}},\n" \
               f"vuosi = {{{vuosi}}},\n" \
               f"}}"

#pitäisi luoda bibtexiin viitteen oikean muotoisena
    
    with open(bib_tiedosto, "a", encoding="utf-8") as f:
        f.write("\n\n" + bibtex_block)

    io.kirjoita(f"lähde '{otsikko}' lisätty.\n")
