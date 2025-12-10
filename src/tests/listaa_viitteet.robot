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


As A User I Want To See All My References By Title
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}
    When Käyttäjä Lisää Viitteen  book  a123  
    ...  Herra Hakkarainen  
    ...  Lisäys
    ...  1000
    ...  Kyllä
    Then Käyttäjä Lisää Viitteen  book  b123 
    ...  Tessa Testaaja  
    ...  Lisäys2
    ...  2000
    ...  Kyllä
    When Käyttäjä Listaa Viitteet Järjestyksessä  abc
    Then Käyttäjä Näkee Tulostuksessa  LÄHDEVIITTEET TEOKSEN NIMEN MUKAAN

As A User I Want To See Errors With Invalid Year Range Inputs
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}
    # Esimerkki viite
    When Käyttäjä Lisää Viitteen  book  testi1  
    ...  Kirjailija  
    ...  Testikirja  
    ...  2010  
    ...  Kyllä
    
    # Syötetään komennot: rajaa -> abc, def -> -5, 2000 -> 2020, 2000 -> 2000, 2020 -> poistu
    When Käyttäjä Antaa Virheellisiä Rajausarvoja
    
    # Tarkistetaan virheilmoitukset
    Then Käyttäjä Näkee Tulostuksessa  VIRHE: Vuosien on oltava kokonaislukuja
    And Käyttäjä Näkee Tulostuksessa   VIRHE: Vuodet eivät voi olla negatiivisia
    And Käyttäjä Näkee Tulostuksessa   VIRHE: Alaraja ei voi olla suurempi kuin yläraja
    
    # Tarkistetaan onnistuminen
    And Käyttäjä Näkee Tulostuksessa   LÄHDEVIITTEET RAJATTU AIKAVÄLILLÄ

As A User I Want To Filter References By Year Range
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}
    # Luodaan testidataa
    When Käyttäjä Lisää Viitteen  book  vanha1990  
    ...  Kirjailija A  
    ...  Vanha Teos  
    ...  1990  
    ...  Kyllä
    Then Käyttäjä Lisää Viitteen  article  sopiva2005  
    ...  Kirjailija B  
    ...  Sopiva Yksi  
    ...  2005  
    ...  Kyllä
    Then Käyttäjä Lisää Viitteen  book  sopiva2020  
    ...  Kirjailija C  
    ...  Sopiva Kaksi  
    ...  2020  
    ...  Kyllä
    Then Käyttäjä Lisää Viitteen  book  uusi2030  
    ...  Kirjailija D  
    ...  Tulevaisuus  
    ...  2030  
    ...  Kyllä
    
    # Syötetään komennot (rajaa -> 2000 -> 2020 -> poistu)
    When Käyttäjä Listaa Viitteet Rajauksella  2000  2020
    
    # Tarkistetaan tulokset
    Then Käyttäjä Näkee Tulostuksessa  LÄHDEVIITTEET RAJATTU AIKAVÄLILLÄ
    And Käyttäjä Näkee Tulostuksessa  Sopiva Yksi
    And Käyttäjä Näkee Tulostuksessa  Sopiva Kaksi