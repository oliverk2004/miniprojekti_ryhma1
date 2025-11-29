*** Settings ***
Library  ../RobotLibrary.py


*** Variables ***
${TEST_BIB_FILE}  test_viitteet.bib


*** Keywords ***
Testausympäristö Asetettu
    Luo Testi Io
    Aseta Testi Tiedosto  ${TEST_BIB_FILE}


Poista Turhat Testitiedostot
    Poista Testi Tiedosto


Tyhjä BibTex Tiedosto
    Luo Tyhja Bib Tiedosto    ${TEST_BIB_FILE}

