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


As A User I Want To See All My References
    Aseta Testi Tiedosto     ${TEST_BIB_FILE}
    Given Käyttäjä Lisää Viitteen  kirja  testi123  
    ...  author=Kirjailija
    ...  title=Testi
    ...  year=2025
    Given Käyttäjä Lisää Viitteen  kirja2  testi1234  
    ...  author=Kirjailija2
    ...  title=Testi2
    ...  year=2026
    When Käyttäjä Listaa Viitteet
    Then Käyttäjä Näkee Tulostuksessa  lähdeviitteet:
    And Käyttäjä Näkee Tulostuksessa  kirja2
    And Käyttäjä Näkee Tulostuksessa  Testi
    And Käyttäjä Näkee Tulostuksessa  testi1234