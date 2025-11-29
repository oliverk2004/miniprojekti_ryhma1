*** Settings ***
Resource  resource.robot
Suite Setup  Testausympäristö Asetettu
Suite Teardown  Poista Turhat Testitiedostot

*** Test Cases ***
As A User I Want To See One Reference
    Given Käyttäjä Lisää Viitteen  kirja  testi123  
    ...  author=Kirjailija
    ...  title=Testi
    ...  year=2025
    When Käyttäjä Listaa Viitteet
    
