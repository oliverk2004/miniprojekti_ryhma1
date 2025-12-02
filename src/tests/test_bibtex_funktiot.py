from src.funktiot.lisaa_viite import lisaa_viite
from src.funktiot.listaa_viitteet import listaa_viitteet
from src.funktiot.poista_viite import poista_viite
from unittest.mock import Mock
from src.StubIO import StubIO

# Ajattelin, että Mock-olioiden hyödyntäminen voisi tässä tapauksessa olla sopiva vaihtoehto...
# Testi, että konsoli tulostaa "Ei lähdeviitteitä", kun viitteitä ei ole bib-tiedostossa.
def test_listaa_viitteet_tyhja(tmp_path):
    tiedosto = tmp_path / "test.bib"
    tiedosto.write_text("", encoding = "utf-8")

    io = StubIO()
    listaa_viitteet(tiedosto, io)

    assert io.output[0] == "Ei lähdeviitteitä.\n"

# Testi, kun tiedostoa ei löydy
def test_file_not_found_error(tmp_path):
    tiedosto = tmp_path / "test.bib"
    # Tiedostoa ei ole luotu, koska .write_text puuttuu

    io = StubIO()
    listaa_viitteet(tiedosto, io)

    assert f"Ei lähdeviitteitä, sillä tiedostoa {tiedosto} ei löytynyt." in io.output[0]

# Testi, kun tallennus peruutetaan.
def test_lisaa_viite_peruutus(tmp_path):
    tiedosto = tmp_path / "test_peruutus.bib"
    alkuperainen_sisalto = "Olemassa oleva viite."
    tiedosto.write_text(alkuperainen_sisalto, encoding="utf-8")
    
    # Syötteet: viite + peruutuskomento "Ei"
    syotteet = [
        "article",
        "PeruutusAvain",
        "Mallikappale, P.",
        "Peruutettu artikkeli",
        "2024",
        "Ei" # PERUUTUS
    ]

    io = StubIO()
    io.input = syotteet

    lisaa_viite(tiedosto, io)

    # Tarkista, että peruutuksen vahvistus tulostui
    viesti_loytyi = False
    odotettu_viesti = "Tallennus peruutettu. Viitettä ei lisätty."
    
    for tuloste in io.output:
        if odotettu_viesti in tuloste:
            viesti_loytyi = True
            break  # Viesti löydetty, ei tarvitse käydä läpi enempää

    assert viesti_loytyi

    # Tarkista, ettei tiedoston sisältö ole muuttunut (eli että alkuperäinen sisältö on yhä sama)
    with open(tiedosto, "r", encoding="utf-8") as f:
        tarkistettu_sisalto = f.read().strip()
    
    assert tarkistettu_sisalto == alkuperainen_sisalto


# Jos vahvistuksessa käyttäjä antaakin jonkin muun kuin "kyllä" tai "ei"
def test_lisaa_viite_tuntematon_vahvistus(tmp_path):
    tiedosto = tmp_path / "test_tuntematon.bib"
    alkuperainen_sisalto = "Olemassa oleva viite."
    tiedosto.write_text(alkuperainen_sisalto, encoding="utf-8")

    syotteet = [
        "article",
        "PeruutusAvain",
        "Mallikappale, P.",
        "Peruutettu artikkeli",
        "2024",
        "Tuntematon",  
        "Ei"            # tarvitaan, koska funktio jatkaa kysymistä
    ]

    io = StubIO()
    io.input = syotteet

    lisaa_viite(tiedosto, io)

    # Tarkista, että tuntematon komento tulostui
    assert any("Tuntematon komento." in tuloste for tuloste in io.output)

    # Tarkista, ettei tiedoston sisältö muuttunut
    with open(tiedosto, "r", encoding="utf-8") as f:
        tarkistettu_sisalto = f.read().strip()

    assert tarkistettu_sisalto == alkuperainen_sisalto


def test_lisaa_viite(tmp_path):
    tiedosto = tmp_path / "test.bib"
    tiedosto.write_text("", encoding="utf-8")

    io = StubIO()
    io.input = [
        "book", 
        "viiteavain", 
        "Ankka, Aku", 
        "Otsikko", 
        "2025", 
        "Kyllä"     # Vahvistus, että viite lisätään. 
    ]

    lisaa_viite(tiedosto, io)

    # Tarkistetaan, että lisääntyy eli "lisätty" tulee tekstinä
    assert any("lisätty" in r for r in io.output)

    with open(tiedosto, "r", encoding="utf-8") as f:
        data = f.read()
        assert "viiteavain" in data
        assert "Otsikko" in data


def test_poista_viite(tmp_path):
    tiedosto = tmp_path / "test.bib"
    tiedosto.write_text("@book{viiteavain, author={Ankka, Aku}, title={Otsikko}, year={2025}}", 
                        encoding="utf-8")

    io = StubIO()
    io.input = [
        "viiteavain", 
        "Kyllä"     # vahvistus, että perutaan
    ]

    poista_viite(tiedosto, io)

    # Tarkistetaan, että poistuu eli "onnistui" tulee tekstinä "Viitteen poistaminen onnistui\n"
    assert any("onnistui" in r for r in io.output)

    # Testataan se, että tiedostossa ei ole enää mitään
    with open(tiedosto, "r", encoding="utf-8") as f:
        data = f.read()
        assert "viiteavain" not in data
        assert "Otsikko" not in data

def test_listaa_viitteet_lajittelee_vuoden_mukaan_vanhimmasta_uusimpaan(tmp_path):
    tiedosto = tmp_path / "test_vuosi.bib"
    
    # Esimerkki viitteiden luonti ja kirjoitus tiedostoon
    viite_a = "@inproceedings{viiteA, author={Author C}, title={Title C}, year={566}}"
    viite_d = "@misc{viiteD, author={Author D}, title={Title D}}" # Vuosi puuttuu. Tulostuu viimeisenä.
    viite_c = "@article{viiteC, author={Author B}, title={Title B}, year={9000}}"
    viite_b = "@book{viiteB, author={Author A}, title={Title A}, year={1000}}"
    # Kirjoitetaan tiedostoon B, A, D, C järjestyksessä
    bibtex_data = f"{viite_b}\n{viite_a}\n{viite_d}\n{viite_c}"    
    tiedosto.write_text(bibtex_data, encoding="utf-8")

    # Käyttäjän syötteet
    io = StubIO()
    io.input = ["vuosi", "poistu"] 
    
    listaa_viitteet(tiedosto, io)

    output_str = "\n".join(io.output) 

    # Tarkistetaan lajitteluotsikko
    assert "LÄHDEVIITTEET JULKAISUVUODEN MUKAAN" in output_str  
    
    # Etsitään viiteavaimien ensimmäiset esiintymät tulosteesta. Odotettu järjestys on vanhin ilmestymisvuosi ensin. 
    # Muuttujiin palautuu viitteiden indeksi arvo kokonaistulostuksesta.
    index_D = output_str.find("viiteD")
    index_C = output_str.find("viiteC")
    index_A = output_str.find("viiteA")
    index_B = output_str.find("viiteB")
    
    # Tarkistetaan järjestys
    assert index_A < index_B
    assert index_B < index_C
    assert index_C < index_D


def test_listaa_viitteet_lajittelee_authorin_nimen_mukaan(tmp_path):
    tiedosto = tmp_path / "test_nimi.bib"
    
    # Esimerkki viitteiden luonti ja kirjoitus tiedostoon
    viite_a = "@article{viiteA, author={JJJJ}, title={Title B}, year={2023}}"
    viite_b = "@book{viiteB, author={MMM, AAA}, title={Title A}, year={2020}}"
    viite_c = "@misc{viiteC, author={zzzzasd, Aino}, title={Title D}}"    
    viite_d = "@inproceedings{viiteD, title={Title C}, year={2018}}" # ei authoria
    # Kirjoitetaan tiedostoon D, C, A, B järjestyksessä
    bibtex_data = f"{viite_d}\n{viite_c}\n{viite_a}\n{viite_b}"
    tiedosto.write_text(bibtex_data, encoding="utf-8")

    # Käyttäjän syötteet
    io = StubIO()
    io.input = ["nimi", "poistu"] 
    
    listaa_viitteet(tiedosto, io)

    output_str = "\n".join(io.output) 

    # Tarkistetaan, että oikea lajitteluotsikko tulostui
    assert "LÄHDEVIITTEET KIRJOITTAJAN NIMEN MUKAAN" in output_str   

    # Etsitään viiteavaimien ensimmäiset esiintymät tulosteesta.
    index_B = output_str.find("viiteB")
    index_A = output_str.find("viiteA")
    index_D = output_str.find("viiteD")
    index_C = output_str.find("viiteC")
   
    # Tarkistetaan järjestys. Aakkosjärjestys teosten kirjoittajien mukaan.
    assert index_A < index_B
    assert index_B < index_C
    assert index_C < index_D

def test_listaa_viitteet_lajittelee_otsikon_mukaan(tmp_path):
    tiedosto = tmp_path / "test_otsikko.bib"
    
    # Esimerkki viitteiden luonti ja kirjoitus tiedostoon
    viite_b = "@article{viiteB, author={Author B}, title={FFFFFFFF}, year={2023}}"
    viite_a = "@book{viiteA, author={Author A}, title={aaa aaa}, year={2005}}"
    viite_d = "@misc{viiteD, author={Author D}}" # ei titleä
    viite_c = "@inproceedings{viiteC, author={Author C}, title={Maailman kartta}, year={1997}}"    
    # Kirjoitetaan tiedostoon B, A, D, C järjestyksessä
    bibtex_data = f"{viite_b}\n{viite_a}\n{viite_d}\n{viite_c}"
    tiedosto.write_text(bibtex_data, encoding="utf-8")

    io = StubIO()
    io.input = ["abc", "poistu"] 
    
    listaa_viitteet(tiedosto, io)

    output_str = "\n".join(io.output) 

    # Tarkistetaan, että oikea lajitteluotsikko tulostui
    assert "LÄHDEVIITTEET TEOKSEN NIMEN MUKAAN" in output_str     
   
    # Etsitään viiteavaimien ensimmäiset esiintymät tulosteesta
    index_B = output_str.find("viiteB")
    index_C = output_str.find("viiteC")
    index_A = output_str.find("viiteA")
    index_D = output_str.find("viiteD")
   
    # Tarkistetaan järjestys. Odotettu järjestys (Aakkosjärjestys otsikon mukaan, puuttuva viimeisenä):
    assert index_A < index_B
    assert index_B < index_C
    assert index_C < index_D


def test_listaa_viitteet_lajittelee_avaimen_mukaan(tmp_path):
    tiedosto = tmp_path / "test_avain.bib"
    
    # Esimerkki viitteiden luonti ja kirjoitus tiedostoon
    viite_b = "@article{bavain, author={Author B}, title={Title B}, year={2023}}"
    viite_c = "@inproceedings{cavain, author={Author C}, title={Title C}, year={1997}}"
    viite_a = "@book{aavain, author={Author A}, title={Title A}, year={2005}}"
    
    # Kirjoitetaan tiedostoon B, C, A järjestyksessä
    bibtex_data = f"{viite_b}\n{viite_c}\n{viite_a}"
    tiedosto.write_text(bibtex_data, encoding="utf-8")

    io = StubIO()
    io.input = ["avain", "poistu"] 
    
    listaa_viitteet(tiedosto, io)

    output_str = "\n".join(io.output) 

    # Tarkistetaan, että oikea lajitteluotsikko tulostui
    assert "LÄHDEVIITTEET VIITEAVAIMEN MUKAAN" in output_str 
    
    # Etsitään viiteavaimien ensimmäiset esiintymät tulosteesta
    index_A = output_str.find("aavain")
    index_B = output_str.find("bavain")
    index_C = output_str.find("cavain")
   
    # Tarkistetaan järjestys: A < B < C
    assert index_A < index_B
    assert index_B < index_C