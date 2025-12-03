import os
from funktiot.lisaa_viite import lisaa_viite
from funktiot.listaa_viitteet import listaa_viitteet
from funktiot.poista_viite import poista_viite
from funktiot.konsoli_IO import KonsoliIO

HAKEMISTO = os.path.dirname(os.path.abspath(__file__))
BIBFILE = os.path.join(HAKEMISTO, "viitteet.bib")

#BIBFILE = "viitteet.bib"

def main():
    io = KonsoliIO()
    io.kirjoita("\nTervetuloa lähdeviite työkaluun!")
    while True:
        io.kirjoita("Haluatko lisätä lähdeviitteen, listata lähdeviitteesi, " +
                    "poistaa lähdeviitteen vai lopettaa?")

        valitse = io.lue("> ").strip().lower()

        if valitse == "lisää":
            lisaa_viite(BIBFILE, io)
            continue
        if valitse == "listaa":
            listaa_viitteet(BIBFILE, io)
            continue
        if valitse == "poista":
            poista_viite(BIBFILE, io)
            continue
        if valitse == "lopeta":
            io.kirjoita("Heippa!\n")
            return
        io.kirjoita("en tiedä mitä tarkoitat :(\n")

if __name__ == "__main__":
    main()
