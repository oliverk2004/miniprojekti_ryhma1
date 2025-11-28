from pybtex.database import BibliographyData, Entry
from .konsoli_IO import KonsoliIO
from .bibtex_funktiot import lataa_bibtex_tiedosto, tallenna, parsi_bibtex

def lisaa_viite(bib_tiedosto, konsoli: KonsoliIO):

    konsoli.kirjoita("lisätään uusi lähdeviite.")
    tyyppi = konsoli.lue("Tyyppi: ").strip().lower()

    # Lataa olemassa olevat viitteet viitteet.bib tiedostosta
    bib_data = lataa_bibtex_tiedosto(bib_tiedosto)

    viiteavain = lisaa_viiteavain(konsoli, bib_data)
    if viiteavain is None:
        return
    
    kentät = lisaa_viitteen_tiedot(konsoli)
    
    # Luodaan Entry-objekti pybtexillä, joka kuvaa yhtä BibTex-viitettä
    # Pitäisi olla myös hyvä oliosuuntauneisuuden kannalta...
    entry = Entry(tyyppi, fields=kentät)
    
    if vahvista(konsoli, viiteavain, entry):
        tallenna_lisays(konsoli, viiteavain, entry, bib_tiedosto, bib_data)

def lisaa_viiteavain(konsoli, bib_data):
    while True:
        viiteavain = konsoli.lue("Viiteavain: ").strip()
        if not viiteavain:
            konsoli.kirjoita("Virhe: Viiteavain ei voi olla tyhjä.\n")
            continue
        
        if bib_data is None:
            # Taas tein tämän, jos ei olisi viitteet.bib tiedostoa jo luotuna
            bib_data = BibliographyData()
        
        if viiteavain in bib_data.entries:
            konsoli.kirjoita(f"Virhe: Viiteavain '{viiteavain}' on jo käytössä.\n")
            continue
        return viiteavain
    
def lisaa_viitteen_tiedot(konsoli):
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
    return kentät

def vahvista(konsoli, viiteavain, entry):
    # Näytä esikatselu
    temp_bib = BibliographyData(entries={viiteavain: entry})
    bibtex_preview = parsi_bibtex(temp_bib)
    
    # Varmistus
    while True:
        konsoli.kirjoita("Syöttämäsi tiedot:")
        konsoli.kirjoita(bibtex_preview)
        
        varmistus = konsoli.lue('Haluatko tallentaa seuraavan viitteen? Kirjoita "Kyllä" tai "Ei".\n> ')
        
        if varmistus.lower() == "ei":
            konsoli.kirjoita("Tallennus peruutettu. Viitettä ei lisätty.\n")
            return False
        elif varmistus.lower() == "kyllä":
            return True
        else:
            konsoli.kirjoita('Tuntematon komento.\n')
            continue

def tallenna_lisays(konsoli, viiteavain, entry, bib_tiedosto, bib_data):

    # Lisää uusi viite viitteet.bib
    bib_data.entries[viiteavain] = entry
    
    otsikko = entry.fields.get('title', 'Otsikkoa ei syötetty')
    # Tallenna tiedostoon
    try:
        tallenna(bib_tiedosto, bib_data)
        konsoli.kirjoita(f"lähde '{otsikko}' lisätty.\n")
    except Exception as e:
        konsoli.kirjoita(f"Virhe tallennuksessa: {e}\n")