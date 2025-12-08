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
    [Arguments]    ${tyyppi}    ${viiteavain}    ${author}    ${title}    ${year}    ${vahvistus}
    Aseta Syotteet     ${tyyppi}    ${viiteavain}    ${author}    ${title}    ${year}    ${vahvistus}
    Call Lisaa Viite


Käyttäjä Listaa Viitteet Järjestyksessä
    [Arguments]    ${järjestys}
    Aseta Syotteet    ${järjestys}  poistu
    Call Listaa Viitteet


Käyttäjä Listaa Viitteet
    Käyttäjä Listaa Viitteet Järjestyksessä  avain


Käyttäjä Näkee Tulostuksessa
    [Arguments]    ${teksti}
    Tuloste Pitaisi Olla    ${teksti}


Käyttäjä Hakee Yksittäisen Viitteen
    [Arguments]    ${viiteavain}
    Aseta Syotteet    ${viiteavain}    peru
    Call Hae Viite