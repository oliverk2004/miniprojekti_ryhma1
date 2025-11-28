
from funktiot.lisaa_viite import lisaa_viite
from funktiot.listaa_viitteet import listaa_viitteet
from funktiot.konsoli_IO import KonsoliIO

import os

HAKEMISTO = os.path.dirname(os.path.abspath(__file__))
BIBFILE = os.path.join(HAKEMISTO, "viitteet.bib")

#BIBFILE = "viitteet.bib"

def main():
    io = KonsoliIO()
    io.kirjoita("\nTervetuloa lähdeviite työkaluun!")
    while True:
        io.kirjoita("Haluatko lisätä lähdeviitteen, listata lähdeviitteesi vai lopettaa?")
        
        valitse = io.lue("> ").strip()

        if valitse == "lisää":
            lisaa_viite(BIBFILE, io)
            continue
        elif valitse == "listaa":
            listaa_viitteet(BIBFILE, io)
            continue
        elif valitse == "lopeta":
            io.kirjoita("Heippa!\n")
            return
        else:
            io.kirjoita("en tiedä mitä tarkoitat :(\n")

if __name__ == "__main__":
    main()