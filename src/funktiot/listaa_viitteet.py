from collections import OrderedDict
from pybtex.database import BibliographyData
from .konsoli_IO import KonsoliIO
from .bibtex_funktiot import lataa_bibtex_tiedosto, parsi_bibtex, onko_olemassa

def listaa_viitteet(bib_tiedosto, konsoli: KonsoliIO):
    bib_data = lataa_bibtex_tiedosto(bib_tiedosto)

    if not onko_olemassa(bib_tiedosto, bib_data, konsoli):
        return

    # Käyttäjän UI. Loopissa voi pyytää eri listaus tapoja viitteille.
    while True:
        konsoli.kirjoita("Käytä seuraavia komentoja viitteiden " \
        "listaamiseen valitsemasi kriteerin perusteella:")
        konsoli.kirjoita("avain (Aakkosjärjestys viitteiden viiteavainten mukaan)")
        konsoli.kirjoita("abc (Aakkosjärjestys teoksen nimen mukaan)")
        konsoli.kirjoita("nimi (Aakkosjärjestys teoksen julkaisija mukaan)")
        konsoli.kirjoita("vuosi (viitteet vanhimmasta uusimpaan)")
        konsoli.kirjoita("rajaa (Listaa viitteet annetun kahden vuoden [min-max] väliltä)")
        konsoli.kirjoita("poistu (poistu viitteiden listauksesta)")

        min_vuosi = None
        max_vuosi = None

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
        elif varmistus.lower() == "rajaa":
            min_vuosi, max_vuosi = hanki_vuosirajat(konsoli)
            konsoli.kirjoita("LÄHDEVIITTEET RAJATTU AIKAVÄLILLÄ.")
            data_tulostukseen = jarjesta_komennon_mukaan(bib_data, 'rajaa', min_vuosi, max_vuosi)
        elif varmistus.lower() == "poistu":
            break
        else:
            konsoli.kirjoita("Tuntematon komento.")
            konsoli.kirjoita("Kirjoita avain, abc, nimi, vuosi, rajaa tai poistu")
            continue
        # Viitteiden tulostus käyttäjän haluaman järjestyksen perusteella.
        bibtex_str = parsi_bibtex(data_tulostukseen)
        konsoli.kirjoita(bibtex_str)

# Funktio, joka määrittää minkä kriteerin mukaan viitteet lajitellaan.
def jarjesta_komennon_mukaan(bib_data: BibliographyData,
    kentta: str, min_str=None, max_str=None) -> BibliographyData:

    # Valitaan oikea lajittelukriteeri
    if kentta == 'nimi':
        # Viitteen julkaisijan nimen perusteella tehtävä lajittelu on
        # monimutkaisempi ja käyttää omaa alifunktiotaan.
        lajittelu_key = hanki_nimien_lajitteluarvo
    # Lajittelu viitteen avaimen mukaan
    elif kentta == 'avain':
        lajittelu_key = lambda item: item[0].lower()
    # Lajittelu viitteen teoksen nimen mukaan
    elif kentta == 'abc':
        lajittelu_key = lambda item: item[1].fields.get('title', '~').lower()
    # Lajittelu viitteen julkaisuvuoden mukaan
    elif kentta == 'vuosi':
        lajittelu_key = hanki_vuosi_lajitteluarvo_vanhin_ensin
    elif kentta == 'rajaa':
        min_vuosi = int(min_str)
        max_vuosi = int(max_str)
        return rajaa_vuodet(bib_data, min_vuosi, max_vuosi)
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
        # Tyhjän sukunimen arvoksi asetetaan aakkosjärjestyksessä '{'. Tulee ennen '~'
        # merkkiä mutta ennen kaikkia kirjamia.
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
# Funktio rajaa viitteistä käyttäjän antamien vuosien perusteella halutut viitteet
def rajaa_vuodet(bib_data, min_vuosi, max_vuosi):
    suodatetut_itemit = OrderedDict()

    for key, entry in bib_data.entries.items():
        # Haetaan vuosi. Oletusarvona None jos puuttuu
        vuosi_str = entry.fields.get('year')

        # Tarkistetaan onko vuosi olemassa ja onko se numero
        if vuosi_str and vuosi_str.isdigit():
            vuosi = int(vuosi_str)
            # Tarkistetaan osuuko vuosi annetulle välille
            if min_vuosi <= vuosi <= max_vuosi:
                suodatetut_itemit[key] = entry

    return BibliographyData(suodatetut_itemit)

# Apufunktio, joka tarkastaa vuosien rajat 'rajaa' komennolle.
def hanki_vuosirajat(konsoli):
    # Tarkastetaan, että käyttäjän antamat vuodet ovat hyväksyttyjä arvoja
    while True:
        min_str = konsoli.lue("Anna alaraja vuosi: \n> ")
        max_str = konsoli.lue("Anna yläraja vuosi: \n> ")

        # vuosien oltava numeroita
        try:
            min_v = int(min_str)
            max_v = int(max_str)
        except ValueError:
            konsoli.kirjoita("VIRHE: Vuosien on oltava kokonaislukuja (esim. 2000).")
            continue

        # vuosien oltava positiivisia
        if min_v < 0 or max_v < 0:
            konsoli.kirjoita("VIRHE: Vuodet eivät voi olla negatiivisia.")
            continue
        # Alaraja vuosille ei voi olla suurempi kuin yläraja.
        if min_v > max_v:
            konsoli.kirjoita("VIRHE: Alaraja ei voi olla suurempi kuin yläraja!")
            continue
        return min_v, max_v
