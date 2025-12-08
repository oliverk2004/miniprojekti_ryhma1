*** Settings ***
Resource  resource.robot
Suite Setup  Testausympäristö Asetettu
Suite Teardown  Poista Turhat Testitiedostot


*** Test Cases ***
As A User I Want To Search One Reference
    Aseta Testi Tiedosto    ${TEST_BIB_FILE}
    When Käyttäjä Lisää Viitteen  book  testi111  
    ...  Kirjailija
    ...  Testi
    ...  2025
    ...  Kyllä
    When Käyttäjä Hakee Yksittäisen Viitteen    testi111
    Then Käyttäjä Näkee Tulostuksessa    testi111
