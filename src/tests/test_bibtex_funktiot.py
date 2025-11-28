from src.funktiot.lisaa_viite import lisaa_viite
from src.funktiot.listaa_viitteet import listaa_viitteet
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