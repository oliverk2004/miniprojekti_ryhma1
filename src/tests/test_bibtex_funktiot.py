from projekti.funktiot.bibtex_funktiot import listaa_viitteet, lisaa_viite
from unittest.mock import Mock

# Ajattelin, että Mock-olioiden hyödyntäminen voisi tässä tapauksessa olla sopiva vaihtoehto...
# Testi, että konsoli tulostaa "Ei lähdeviitteitä", kun viitteitä ei ole bib-tiedostossa.
def test_listaa_viitteet_tyhja(tmp_path):
    tiedosto = tmp_path / "test.bib"
    tiedosto.write_text("", encoding = "utf-8")

    io = Mock()
    listaa_viitteet(tiedosto, io)

    io.kirjoita.assert_called_once_with("Ei lähdeviitteitä.\n")


# Testi, että konsoli tulostaa viitteet sisältöineen. 
def test_listaa_viitteet(tmp_path):
    tiedosto = tmp_path / "test.bib"
    tiedosto.write_text("@tyyppi{viiteavain, tekijä={Esimerkki}}", encoding = "utf-8")

    io = Mock()
    listaa_viitteet(tiedosto, io)

    tuloste = io.kirjoita.call_args[0][0]
    assert "lähdeviitteet:" in tuloste
    assert "@tyyppi{viiteavain" in tuloste
