# import os
from funktiot.bibtex_funktiot import lisaa_viite, listaa_viitteet
from funktiot.konsoli_IO import KonsoliIO

BIBFILE = "viitteet.bib"

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