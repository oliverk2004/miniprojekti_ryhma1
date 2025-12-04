*** Settings ***
Resource  resource.robot
Suite Setup  Testausympäristö Asetettu
Suite Teardown  Poista Turhat Testitiedostot

*** Test Cases ***
As A User I Want To See One Reference
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}
    Given Käyttäjä Lisää Viitteen  book  testi123  
    ...  author=Kirjailija
    ...  title=Testi
    ...  year=2025
    ...  vahvistus=Kyllä
    When Käyttäjä Listaa Viitteet
    Then Käyttäjä Näkee Tulostuksessa  book


As A User I Want To See All My References
    Aseta Testi Tiedosto     ${TEST_BIB_FILE}
    Given Käyttäjä Lisää Viitteen  article  testi123  
    ...  author=Kirjailija
    ...  title=Testi
    ...  year=2025
    ...  vahvistus=Kyllä
    Given Käyttäjä Lisää Viitteen  book  testi1234  
    ...  author=Kirjailija2
    ...  title=Testi2
    ...  year=2026
    ...  vahvistus=Kyllä
    When Käyttäjä Listaa Viitteet
    Then Käyttäjä Näkee Tulostuksessa  article
    And Käyttäjä Näkee Tulostuksessa  book
    And Käyttäjä Näkee Tulostuksessa  Testi
    And Käyttäjä Näkee Tulostuksessa  testi1234