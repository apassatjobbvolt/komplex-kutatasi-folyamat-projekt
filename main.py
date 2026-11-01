import time
import random
import csv
import json

# DAG

dag = {
    "cache_betoltes": [],
    "meres": ["cache_betoltes"],
    "ellenorzes": ["meres"],
    "kiertekeles": ["ellenorzes"],
    "nyers_export": ["ellenorzes"],
    "exportalas": ["kiertekeles"]
}

# DAG elemek:

# Cache betoltese - kimenet: "mereseredmeny" ha cache-bol dolgozik tovabb, "None" ha nem 
def cache_betoltes(fajlnev):
    mereseredmeny = betoltcache(fajlnev)
    if mereseredmeny != None:
        kerdes = str(input("Folytatas cache-bol? I/N: ").upper)
        while kerdes not in ("I", "N"):
                    kerdes = str(input("Nem megfelelo bemenet. Folytatas cache-bol? I/N: ").upper())
                    if kerdes == "I" or kerdes == "N":
                        break
        if kerdes == "I":
            print("Folytatas cache-bol...")
            return mereseredmeny
        else:
            print("Folytatas uj meressel...")
            return None
    else:
        return None

# Meres, egyellore API szimulalt - meresek szamat, meresek kozotti idot, min es max kimeneti adatokat ker
def meres(meresszam, meresgyak, hatarmin, hatarmax):
    mereseredmeny = list()
    for i in range(1,meresszam+1):
        mereseredmeny.append(random.randint(int(hatarmin),int(hatarmax)))
        time.sleep(meresgyak / 1000)
    print(f"Mert ertekek: {mereseredmeny}")
    mentcache(mereseredmeny, "cache_meres")
    return mereseredmeny

# Ellenorzes
def ellenorzes(bemenet, meresszam, hatarmin, hatarmax):
    megfelel = True
    for ertek in bemenet:
        if not (type(ertek) == float or type(ertek) ==int):
            megfelel = False
        if ertek < hatarmin or ertek > hatarmax:
            megfelel = False

    if megfelel == True:
        if meresszam == len(bemenet):
            print("Meresi eredmenyek ellenorzese sikeres.")
        else:
            megfelel = False
            print("Meresi eredmeny ellenorzese sikertelen - mert adatok szama nem egyezik a kert adatmennyiseggel.")
    else:
        print("Meresi eredmenyek ellenorzese sikertelen - mert adatok meresi tartomanyon kivul.")

    if megfelel != True:
        kerdes = str(input("Folytatas hibas adatokkal? I/N: ").upper())
        while kerdes not in ("I", "N"):
            kerdes = str(input("Nem megfelelo bemenet. Folytatas hibas adatokkal? I/N: ").upper())
            if kerdes == "I" or kerdes == "N":
                break
        folytatas = False
        if kerdes == "I":
            print("A program tovabbmegy az esetlegesen hibas adatokkal")
            folytatas = True
        else:
            print("A program leall")

    if megfelel == True:
        folytatas = True

    return folytatas
            
# kiertekeles fgv-k:
def atlag(bemenet):
    return sum(bemenet) / len(bemenet)

# exportalas

def exportalas(bemenet, fajlnev):
    fieldnames = list()
    for adat in bemenet:
        fieldnames.append(adat)
    with open(f"{fajlnev}.csv", "w", newline="", encoding="utf-8") as csvfile:
        iras = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        iras.writeheader()
        iras.writerow(bemenet)
    print("Exportalas sikeres")

# DAG elemek vege

# cache

def mentcache(bemenet, fajlnev):
    with open(f"{fajlnev}.json", "w", encoding="utf-8") as jsonfile:
        json.dump(bemenet, jsonfile)

def betoltcache(fajlnev):
    try:
        with open(f"{fajlnev}.json", "r", encoding="utf-8") as jsonfile:
            return json.load(jsonfile)
    except FileNotFoundError:
        return None

#teszter:

mereseredmeny = meres(10,10,101,140)
folytatas = ellenorzes(mereseredmeny, 9, 101, 140)
if folytatas == True:
    adatok = {"Atlag": atlag(mereseredmeny), "Minimum": min(mereseredmeny), "Maximum": max(mereseredmeny)}
    exportalas(adatok, "eredmeny")