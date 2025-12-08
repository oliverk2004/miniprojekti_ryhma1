*** Settings ***
Resource  resource.robot
Suite Setup  Testausympäristö Asetettu
Suite Teardown  Poista Turhat Testitiedostot



*** Test Cases ***
As A User I Want To Add One Reference
    Aseta Testi Tiedosto    ${TEST_BIB_FILE}
    When Käyttäjä Lisää Viitteen  book  lisätään123  
    ...  Lisääjä  
    ...  Lisäys
    ...  1234
    ...  Kyllä
    When Käyttäjä Listaa Viitteet
    Then Käyttäjä Näkee Tulostuksessa  book