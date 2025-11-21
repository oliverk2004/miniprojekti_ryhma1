import os
BIBFILE = "viitteet.bib"

def listaa_viitteet(bib_tiedosto):
    try:
        with open(bib_tiedosto, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            print("Ei lähdeviitteitä.\n")
            return
        
        print("lähdeviitteet:")
        print(content)
    except FileNotFoundError:
        print(f"Ei lähdeviitteitä, sillä tiedostoa {bib_tiedosto} ei löytynyt.\n")

def lisaa_viite(bib_tiedosto):
    print("lisätään uusi lähdeviite.")
    tyyppi = input("Tyyppi: ")
    viiteavain = input("Viiteavain: ")
    tekijä = input("Tekijät: ").strip()
    otsikko = input("Otsikko: ").strip()
    vuosi = input("Vuosi: ")

#tähän muut tärkeät tiedot jos esim doi tarvitsee tai muuta
    
    bibtex_block = f"@{tyyppi}{{{viiteavain},\n" \
               f"tekijä = {{{tekijä}}},\n" \
               f"otsikko = {{{otsikko}}},\n" \
               f"vuosi = {{{vuosi}}},\n" \
               f"}}"

#pitäisi luoda bibtexiin viitteen oikean muotoisena
    
    with open(bib_tiedosto, "a", encoding="utf-8") as f:
        f.write("\n\n" + bibtex_block)

    print(f"lähde '{otsikko}' lisätty.\n")

def main():
    print("\nTervetuloa lähdeviite työkaluun!")
    while True:
        print("Haluatko lisätä lähdeviitteen, listata lähdeviitteesi vai lopettaa?")
        
        valitse = input ("> ").strip()

        if valitse == "lisää":
            lisaa_viite(BIBFILE)
            continue
        elif valitse == "listaa":
            listaa_viitteet(BIBFILE)
            continue
        elif valitse == "lopeta":
            print("Heippa!\n")
            return
        else:
            print("en tiedä mitä tarkoitat :(\n")

if __name__ == "__main__":
    main()