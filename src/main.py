import os
from funktiot.lisaa_viite import lisaa_viite
from funktiot.listaa_viitteet import listaa_viitteet
from funktiot.yksittainen_viite import listaa_yksittainen_viite
from funktiot.poista_viite import poista_viite
from funktiot.konsoli_IO import KonsoliIO

HAKEMISTO = os.path.dirname(os.path.abspath(__file__))
BIBFILE = os.path.join(HAKEMISTO, "viitteet.bib")

#BIBFILE = "viitteet.bib"

def main():
    io = KonsoliIO()
    io.kirjoita("\nTervetuloa lähdeviite työkaluun!")
    while True:
        io.kirjoita("Haluatko lisätä lähdeviitteen, listata lähdeviitteesi, hakea yksittäisen viitteen, " +
                    "poistaa lähdeviitteen vai lopettaa?")

        valitse = io.lue("> ").strip().lower()

        if valitse == "lisää":
            lisaa_viite(BIBFILE, io)
            continue
        if valitse == "listaa":
            listaa_viitteet(BIBFILE, io)
            continue
        if valitse == "hae":
            listaa_yksittainen_viite(BIBFILE, io)
            continue
        if valitse == "poista":
            poista_viite(BIBFILE, io)
            continue
        if valitse == "lopeta":
            io.kirjoita("Heippa!\n")
            return
        io.kirjoita("en tiedä mitä tarkoitat :(\n")
        io.kirjoita("Valitse joku näistä komennoista:")
        io.kirjoita("lisää | listaa | hae | poista | lopeta\n")

if __name__ == "__main__":
    main()
