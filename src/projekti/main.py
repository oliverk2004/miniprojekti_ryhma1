import os
BIBFILE = "viitteet.bib"

def listaa_viitteet():
    with open(BIBFILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        print("Ei lähdeviitteitä.")
        return
    
    print("lähdeviitteet:")
    print(content)



def lisaa_viite():
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
    
    with open(BIBFILE, "a", encoding="utf-8") as f:
        f.write("\n\n" + bibtex_block)

    print(f"lähde '{otsikko}' lisätty.")

def main():
    print("Tervetuloa lähdeviite työkaluun!")
    print("Haluatko lisätä lähdeviitteen, listata lähdeviitteesi vai lopettaa?")
    
    valitse = input ("> ").strip()

    if valitse == "lisää":
        lisaa_viite()
    elif valitse == "listaa":
        listaa_viitteet()
    elif valitse == "lopeta":
        print("Heippa!")
    else:
        print("en tiedä mitä tarkoitat :(")

if __name__ == "__main__":
    main()