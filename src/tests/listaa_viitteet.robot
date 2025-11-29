*** Settings ***
Resource  resource.robot
Suite Setup  Testausympäristö Asetettu
Suite Teardown  Poista Turhat Testitiedostot

*** Test Cases ***
As A User I Want To See One Reference
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}
    Given Käyttäjä Lisää Viitteen  kirja  testi123  
    ...  author=Kirjailija
    ...  title=Testi
    ...  year=2025
    When Käyttäjä Listaa Viitteet
    Then Käyttäjä Näkee Tulostuksessa  lähdeviitteet:
    And Käyttäjä Näkee Tulostuksessa  kirja

