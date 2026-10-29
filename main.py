import time
import random
import csv

# lepesek: meres, kiertekeles, exportalas
#hianyos: DAG, valos API kezelese, Hibatures/Caching

#DAG:
#   Meres

#API szimulator
def meres():
    mereseredmeny = list()
    n = int(input("Meresek szama: "))
    t = int(input("Meres gyakorisaga (ms): "))
    for i in range(1,n+1):
        mereseredmeny.append(random.randint(100,130))
        time.sleep(t / 1000)
    print(f"Mert ertekek: {mereseredmeny}")
    return mereseredmeny

# kiertekeles fgv-k:
def atlag(bemenet):
    return sum(bemenet) / len(bemenet)

# exportalas

def exportalas(adatok, fajlnev):
    fieldnames = list()
    for adat in adatok:
        fieldnames.append(adat)
    with open(f"{fajlnev}.csv", "w", newline="", encoding="utf-8") as csvfile:
        iras = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        iras.writeheader()
        iras.writerow(adatok)
    print("Exportalas sikeres")


#teszter:

mereseredmeny = meres()
adatok = {"Atlag": atlag(mereseredmeny), "Minimum": min(mereseredmeny), "Maximum": max(mereseredmeny)}
exportalas(adatok, "eredmeny")