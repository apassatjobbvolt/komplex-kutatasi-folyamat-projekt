# komplex-kutatasi-folyamat-projekt
Python programozás projektfeladat

Hasznalathoz PySerial telepitese szukseges

meroeszkoz: OHAUS Scout STX6201 precizios merleg
meres lehet: kulonbozo erok vagy valtozo sulyero merese, peldaul: aramlastan - arkhimedesz torvenyenek igazolasa merleggel - meresek vegzese suly mozgatasa kozben, itt a min es max kimenet lesz mervado
COM port beallitasa szukseges lehet - Windows rendszeru szamitogep eseten Windows eszkozkezeloben - mas operacios rendszerek eseteben tovabbi informacio a meroeszkoz dokumentaciojaban talalhato.
API integracio a meroeszkoz dokumentacioja alapjan: www.hogentogler.com/images/Ohaus_30268984_Scout_USB_Device_manual.pdf
Egyeb felhasznalt irodalom:
https://www.w3schools.com/python/python_lists.asp
https://www.w3schools.com/python/python_while_loops.asp
https://www.w3schools.com/python/python_dictionaries.asp
https://www.w3schools.com/python/module_random.asp
https://docs.python.org/3/library/csv.html

Mukodes:
A program a fent emlitett meroeszkozzel valo ciklikus meresek rogzitesere es kiertekelesere alkalmas. Meroeszkoz hianyaban a program tesztelesere meroeszkoz szimulatorral is rendelkezik.
Amennyiben kesz vagy megszakadt meres tortent elozoleg, a program felajanlja az ezen meresbol szarmazo adatokkal valo munkat.
A mereteket a meroeszkoz specifikacioja szerinti merestartomannyal, illetve a kert meresi ertekek szamaval hasonlitja ossze a kapott adatokat ellenorzes gyanant.
Kimenetkent .csv fajlt kapunk.
