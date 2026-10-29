import time
import random
import csv

# lepesek: meres, kiertekeles, exportalas
#hianyos: DAG, valos API kezelese, Hibatures/Caching

#DAG

dag = {
    "meres": [],
    "ellenorzes": ["meres"],
    "kiertekeles": ["ellenorzes"],
    "nyers_export": ["ellenorzes"],
    "exportalas": ["kiertekeles"]
}

# Meres, egyellore API szimulalt - meresek szamat, meresek kozotti idot, min es max kimeneti adatokat ker
def meres(meresszam, meresgyak, hatarmin, hatarmax):
    mereseredmeny = list()
    for i in range(1,meresszam+1):
        mereseredmeny.append(random.randint(int(hatarmin),int(hatarmax)))
        time.sleep(meresgyak / 1000)
    print(f"Mert ertekek: {mereseredmeny}")
    return mereseredmeny

# Ellenorzes
def ellenorzes(bemenet, meresgyak, hatarmin, hatarmax):
    megfelel = True
    for ertek in bemenet:
        if not (type(ertek) == float or type(ertek) ==int):
            megfelel = False
        if ertek < hatarmin or ertek > hatarmax:
            megfelel = False
    if megfelel == True:
        if meresgyak == len(bemenet):
            print("Meresi eredmenyek ellenorzese sikeres.")
        else:
            print("Meresi eredmeny ellenorzese sikertelen - mert adatok szama nem egyezik a kert adatmennyiseggel. Nyers adatok exportalasa cache-be...")
    else:
        print("Meresi eredmenyek ellenorzese sikertelen - mert adatok meresi tartomanyon kivul. Nyers adatok exportalasa cache-be...")
#   mentcache(bemenet, "cache_ellenorzes") - ez egy fgv. lesz, exportalas fgv-hez hasonlo, csak szotar helyett listat kezel majd (exportalas fuggyveny csak dict-et tud kezelni jelenleg)
    if megfelel != True:
        kerdes = str(input("Folytatas hibas adatokkal? I/N: "))
        while kerdes != "I" or kerdes != "N":
            kerdes = str(input("Nem megfelelo bemenet. Folytatas hibas adatokkal? I/N: "))
            if kerdes == "I" or kerdes == "N":
                break
    folytatas = False
    if kerdes == "I":
        print("A program tovabbmegy az esetlegesen hibas adatokkal")
        folytatas = True
    else:
        print("A program leall")
    return folytatas
            



# kiertekeles fgv-k:
def atlag(bemenet):
    return sum(bemenet) / len(bemenet)

# exportalas

def exportalas(adatokbe, fajlnev):
    fieldnames = list()
    for adat in adatokbe:
        fieldnames.append(adat)
    with open(f"{fajlnev}.csv", "w", newline="", encoding="utf-8") as csvfile:
        iras = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        iras.writeheader()
        iras.writerow(adatokbe)
    print("Exportalas sikeres")


#teszter:

mereseredmeny = meres(10,10,101,140)
folytatas = ellenorzes(mereseredmeny, 9, 101, 140)
if folytatas == True:
    adatok = {"Atlag": atlag(mereseredmeny), "Minimum": min(mereseredmeny), "Maximum": max(mereseredmeny)}
    exportalas(adatok, "eredmeny")