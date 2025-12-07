*** Settings ***
Resource  resource.robot
Suite Setup  Testausympäristö Asetettu
Suite Teardown  Poista Turhat Testitiedostot

*** Test Cases ***
As A User I Want To See One Reference
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}
    When Käyttäjä Lisää Viitteen  book  testi123  
    ...  Kirjailija
    ...  Testi
    ...  2025
    ...  Kyllä
    Then Käyttäjä Näkee Tulostuksessa  book


As A User I Want To See All My References
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}
    When Käyttäjä Lisää Viitteen  book  lisätään123  
    ...  Lisääjä  
    ...  Lisäys
    ...  1234
    ...  Kyllä
    Then Käyttäjä Lisää Viitteen  book  lisätään456 
    ...  Lisääjä2  
    ...  Lisäys2
    ...  1235
    ...  Kyllä
    Aseta Syotteet  tyyppi    Kyllä
    When Käyttäjä Listaa Viitteet
    Then Käyttäjä Näkee Tulostuksessa  book


As A User I Want To See All My References By Year
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}
    When Käyttäjä Lisää Viitteen  article  artikkeli1  
    ...  Lisääjä  
    ...  Lisäys
    ...  1000
    ...  Kyllä
    Then Käyttäjä Lisää Viitteen  book  kirja300 
    ...  Lisääjä2  
    ...  Lisäys2
    ...  2000
    ...  Kyllä
    When Käyttäjä Listaa Viitteet Järjestyksessä  vuosi
    Then Käyttäjä Näkee Tulostuksessa  LÄHDEVIITTEET JULKAISUVUODEN MUKAAN


As A User I Want To See All My References By Author
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}
    When Käyttäjä Lisää Viitteen  article  artikkeli9  
    ...  Herra Hakkarainen  
    ...  Lisäys
    ...  1000
    ...  Kyllä
    Then Käyttäjä Lisää Viitteen  book  kirja321 
    ...  Tessa Testaaja  
    ...  Lisäys2
    ...  2000
    ...  Kyllä
    When Käyttäjä Listaa Viitteet Järjestyksessä  nimi
    Then Käyttäjä Näkee Tulostuksessa  LÄHDEVIITTEET KIRJOITTAJAN NIMEN MUKAAN