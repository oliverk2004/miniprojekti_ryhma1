from .konsoli_IO import KonsoliIO
from .bibtex_funktiot import lataa_bibtex_tiedosto, parsi_bibtex, yrita_lukemista_pythonilla
from collections import OrderedDict
from pybtex.database import BibliographyData

def listaa_viitteet(bib_tiedosto, konsoli: KonsoliIO):
    bib_data = lataa_bibtex_tiedosto(bib_tiedosto)

    if bib_data is None:
        # Tiedostoa ei löydy tai se on virheellinen
        yrita_lukemista_pythonilla(bib_tiedosto, konsoli)
        return
    
    if len(bib_data.entries) == 0:
        konsoli.kirjoita("Ei lähdeviitteitä.\n")
        return
    
    # Käyttäjän UI. Loopissa voi pyytää eri listaus tapoja viitteille.
    while True:
        konsoli.kirjoita("Käytä seuraavia komentoja viitteiden listaamiseen valitsemasi kriteerin perusteella:")
        konsoli.kirjoita("avain (Aakkosjärjestys viitteiden viiteavainten mukaan)")
        konsoli.kirjoita("abc (Aakkosjärjestys teoksen nimen mukaan)")
        konsoli.kirjoita("nimi (Aakkosjärjestys teoksen julkaisija mukaan)")
        konsoli.kirjoita("vuosi (viitteet vanhimmasta uusimpaan)")
        konsoli.kirjoita("poistu (poistu viitteiden listauksesta)")

        varmistus = konsoli.lue("Anna komento: \n> ")

        if varmistus.lower() == "avain":
            konsoli.kirjoita("LÄHDEVIITTEET VIITEAVAIMEN MUKAAN")
            data_tulostukseen = jarjesta_komennon_mukaan(bib_data, 'avain')
        elif varmistus.lower() == "abc":
            konsoli.kirjoita("LÄHDEVIITTEET TEOKSEN NIMEN MUKAAN")
            data_tulostukseen = jarjesta_komennon_mukaan(bib_data, 'abc')
        elif varmistus.lower() == "nimi":
            konsoli.kirjoita("LÄHDEVIITTEET KIRJOITTAJAN NIMEN MUKAAN")
            data_tulostukseen = jarjesta_komennon_mukaan(bib_data, 'nimi')
        elif varmistus.lower() == "vuosi":
            konsoli.kirjoita("LÄHDEVIITTEET JULKAISUVUODEN MUKAAN")
            data_tulostukseen = jarjesta_komennon_mukaan(bib_data, 'vuosi')
        elif varmistus.lower() == "poistu":
            break
        else:
            konsoli.kirjoita("Tuntematon komento. Kirjoita avain, abc, nimi, vuosi tai poistu")
            continue
        # Viitteiden tulostus käyttäjän haluaman järjestyksen perusteella.
        bibtex_str = parsi_bibtex(data_tulostukseen)    
        konsoli.kirjoita(bibtex_str)

# Funktio, joka määrittää minkä kriteerin mukaan viitteet lajitellaan.
def jarjesta_komennon_mukaan(bib_data: BibliographyData, kentta: str) -> BibliographyData:    
    # Valitaan oikea lajittelukriteeri
    if kentta == 'nimi':
        # Viitteen julkaisijan nimen perusteella tehtävä lajittelu on monimutkaisempi ja käyttää omaa alifunktiotaan.
        lajittelu_key = hanki_nimien_lajitteluarvo
        
    # Lajittelu viitteen avaimen mukaan
    elif kentta == 'avain':
        lajittelu_key = lambda item: item[0].lower()
    # Lajittelu viitteen teoksen nimen mukaan    
    elif kentta == 'abc':
        lajittelu_key = lambda item: item[1].fields.get('title', '~').lower()
    # Lajittelu viitteen julkaisuvuoden mukaan    
    elif kentta == 'vuosi':
        # lajittelu_key = lambda item: int(item[1].fields.get('year', 0))   
        lajittelu_key = hanki_vuosi_lajitteluarvo_vanhin_ensin     
    else:
        # Palautetaan alkuperäinen data, jos kenttä on tuntematon
        return bib_data 

    jarjestetyt_itemit = sorted(
        bib_data.entries.items(),
        key=lajittelu_key
    )
    
    jarjestetty_sanasto = OrderedDict(jarjestetyt_itemit)
    return BibliographyData(jarjestetty_sanasto)

# Funktio, joka hakee viitteen julkaisijan nimet
def hanki_nimien_lajitteluarvo(item):
    entry = item[1]
    sukunimi_raw = ""
    etunimi_raw = ""

    kentat_jarjestyksessa = ['author', 'editor']

    # tarkastellaan author kenttä. Jos authoria ei ole, tarkastellaan editor kentän sisältöä.
    for kentan_nimi in kentat_jarjestyksessa:
        # Tarkastetaan onko avain olemassa ja onko sillä sisältöä.
        if kentan_nimi in entry.persons and entry.persons[kentan_nimi]:

            # Poimitaan listasta henkilö, jonka nimeä käytetään lajitteluun
            lajittelu_henkilo = entry.persons[kentan_nimi][0]
            # Last_names on pybtex-objektin lista sukunimistä.
            if lajittelu_henkilo.last_names:
                # Otetaan listan ensimmäinen sukunimi talteen lajittelua varten.
                sukunimi_raw = lajittelu_henkilo.last_names[0]
            # First_names on lista etunimistä
            if lajittelu_henkilo.first_names:
                # Etunimet yhdistetään yhdeksi merkkijonoksi välilyönnillä
                etunimi_raw = " ".join(lajittelu_henkilo.first_names)

            break

    # Määritetään ensisijainen avain sukunimen perusteella
    if sukunimi_raw and not sukunimi_raw.isspace():
        # Jos sukunimi löytyy
        sukunimi_key = sukunimi_raw.lower()
    elif etunimi_raw:
        # Sukunimi puuttuu, mutta etunimi löytyy
        # Tyhjän sukunimen arvoksi asetetaan aakkosjärjestyksessä '{'. Tulee ennen '~' merkkiä mutta ennen kaikkia kirjamia.
        sukunimi_key = "{" 
    else:
        # Author on kokonaan tyhjä. Ei etu eikä sukunimeä.
        # Käytetään merkkiä '~', joka on ASCII aakkosten viimeinen.
        sukunimi_key = "~"

    # Määritetään toissijaiseksi avaimeksi etunimi
    if etunimi_raw:
        etunimi_key = etunimi_raw.lower()
    else:
        etunimi_key = ""

    return (sukunimi_key, etunimi_key)

# Vuosi lajittelun apufunktio.
def hanki_vuosi_lajitteluarvo_vanhin_ensin(item):
    # hae bibtex kentästä "year" arvo
    vuosi_str = item[1].fields.get('year')
    
    # Tarkistetaan, että arvo on olemassa JA on numero
    if vuosi_str and isinstance(vuosi_str, str) and vuosi_str.isdigit():
        # Vanhin ensin. Menee tulostettavan listan alkuun. Palautuu tuple (0, pienin vuosi).
        return (0, int(vuosi_str))
    
    # Vuosi puuttuu tai on virheellinen. Menee tulostettavan listan loppuun. Palautuu tuple (1, 0).
    return (1, 0)