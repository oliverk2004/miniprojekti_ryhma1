*** Settings ***
Resource  resource.robot
Suite Setup  Testausympäristö Asetettu
Suite Teardown  Poista Turhat Testitiedostot



*** Test Cases ***
As A User I Want To Add One Reference
    Aseta Testi Tiedosto    ${TEST_BIB_FILE}
    Given Käyttäjä Lisää Viitteen  book  lisätään123  
    ...  author=Lisääjä  
    ...  title=Lisäys
    ...  year=1234
    When Käyttäjä Listaa Viitteet
    Then Käyttäjä Näkee Tulostuksessa  book
    And Käyttäjä Näkee Tulostuksessa  lisätään123
    And Käyttäjä Näkee Tulostuksessa  Lisääjä
    And Käyttäjä Näkee Tulostuksessa  Lisäys
    And Käyttäjä Näkee Tulostuksessa  1234