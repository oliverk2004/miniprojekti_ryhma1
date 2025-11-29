*** Settings ***
Library  ../RobotLibrary.py


*** Variables ***
${TEST_BIB_FILE}  test_viitteet.bib


*** Keywords ***
Testausympäristö Asetettu
    Luo Testi Io
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}


Poista Turhat Testitiedostot
    Poista Testi Tiedosto


Tyhjä BibTex Tiedosto
    Luo Tyhja Bib Tiedosto    ${TEST_BIB_FILE}


Käyttäjä Lisää Viitteen
    [Arguments]    ${tyyppi}    ${viiteavain}    &{kentät}
    Lisaa Viite Bib Tiedostoon     ${tyyppi}    ${viiteavain}    &{kentät}


Käyttäjä Listaa Viitteet
    Call Listaa Viitteet


Käyttäjä Näkee Tulostuksessa
    [Arguments]    ${teksti}
    Tuloste Pitaisi Olla    ${teksti}