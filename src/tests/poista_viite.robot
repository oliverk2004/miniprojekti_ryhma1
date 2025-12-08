*** Settings ***
Resource  resource.robot
Suite Setup  Testausympäristö Asetettu
Suite Teardown  Poista Turhat Testitiedostot


*** Test Cases ***
AS A User I Want To Remove Reference
    Aseta Testi Tiedosto    ${TEST_BIB_FILE}
    Käyttäjä Lisää Viitteen    tyyppi=article    viiteavain=avain    
    ...    author=testaaja    
    ...    title=testi    
    ...    year=2020
    ...    vahvistus=Kyllä
    Aseta Syotteet    avain    Kyllä
    Call Poista Viitteet
    Käyttäjä Näkee Tulostuksessa    onnistui
