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


# Testi, että konsoli tulostaa viitteet sisältöineen. 
def test_listaa_viitteet(tmp_path):
    tiedosto = tmp_path / "test.bib"
    tiedosto.write_text("@article{viiteavain, author={Esimerkki}, title={Testi}, year={2025}}", 
                        encoding = "utf-8")

    io = StubIO()
    listaa_viitteet(tiedosto, io)

    assert "lähdeviitteet:" in io.output[0]
    assert "@article{viiteavain" in io.output[0]

    assert "viiteavain" in io.output[0]


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


# def test_poista_viite(tmp_path):
