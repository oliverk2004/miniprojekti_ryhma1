from projekti.funktiot.bibtex_funktiot import listaa_viitteet, lisaa_viite
from unittest.mock import Mock

def test_listaa_viitteet_tyhja(tmp_path):
    tiedosto = tmp_path / "test.bib"
    tiedosto.write_text("", encoding = "utf-8")

    io = Mock()
    listaa_viitteet(tiedosto, io)

    io.kirjoita.assert_called_once_with("Ei lähdeviitteitä.\n")