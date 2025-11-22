from projekti.funktiot.bibtex_funktiot import listaa_viitteet, lisaa_viite
from unittest.mock import Mock
from tests.StubIO import StubIO

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
    tiedosto.write_text("@tyyppi{viiteavain, tekijä={Esimerkki}}", encoding = "utf-8")

    io = StubIO()
    listaa_viitteet(tiedosto, io)

    assert "lähdeviitteet:" in io.output[0]
    assert "@tyyppi{viiteavain" in io.output[0]


# Testi, kun tiedostoa ei löydy
def test_file_not_found_error(tmp_path):
    tiedosto = tmp_path / "test.bib"
    # Tiedostoa ei ole luotu, koska .write_text puuttuu

    io = StubIO()
    listaa_viitteet(tiedosto, io)

    assert f"Ei lähdeviitteitä, sillä tiedostoa {tiedosto} ei löytynyt." in io.output[0]
