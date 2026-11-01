import time
import random
import csv
import json
import serial

# fontos!
# cache_betoltes = kulon lepes, felhasznaloi adatbevitelt igenyel
# beoltcache = segedfuggveny redundancia elkerulese erdekeben

# www.hogentogler.com/images/Ohaus_30268984_Scout_USB_Device_manual.pdf
# meroeszkoz: OHAUS Scout STX6201 precizios merleg
# meres: kulonbozo erok vagy valtozo sulyero merese, peldaul:
# aramlastan - arkhimedesz torvenyenek igazolasa merleggel - meresek vegzese suly mozgatasa kozben, itt a min es max kimenet lesz mervado

# Pontos gravitacios gyorsulas a meres helyen:
g = 9.81

# DAG fuggosegek

dag = {
    "cache_betoltes": [],
    "meres": ["cache_betoltes"],
    "ellenorzes": ["meres"],
    "kiertekeles": ["ellenorzes"],
    "exportalas": ["kiertekeles"]
}

# DAG elemek:

# Cache betoltese - kimenet: "mereseredmeny" ha cache-bol dolgozik tovabb, "None" ha nem 
def cache_betoltes(fajlnev):
    mereseredmeny = betoltcache(fajlnev)
    if mereseredmeny != None:
        kerdes = str(input("Folytatas cache-bol? I/N: ").upper())
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
    for i in range(0,meresszam):
        mereseredmeny.append(random.randint(int(hatarmin),int(hatarmax)))
        time.sleep(meresgyak)
    print(f"Mert ertekek: {mereseredmeny}")
    mentcache(mereseredmeny, "cache_meres")
    return mereseredmeny

# COM port atallitasa (Windows szamitogep eseten) Windows Eszkozkezeloben, illetve helyben is szukseges lehet
# mas operacios rendszer eseten tovabbi informacio a meroeszkoz dokumentaciojaban talalhato
def valosmeres(meresszam, meresgyak, com_port="COM5"):
    mereseredmeny = list()

    with serial.Serial(port=com_port, baudrate=9600, bytesize=8, parity="N", stopbits=1, timeout=2) as meroeszkoz:
        meroeszkoz.reset_input_buffer()
        for i in range(0,meresszam):
            meroeszkoz.write(b"IP\r\n")
            bemenet = meroeszkoz.readline().decode("ascii").strip()
            kimenet = float(bemenet[:11].replace("*", " ").strip())
            # meroeszkoz kimeneteben az elso 11 karakter maga a suly, ures karakterek pedig "*"-gal vannak kitoltve
            mereseredmeny.append(kimenet / 1000 * g)
            # meroeszkoz gramm-ban adja meg a mert erteket - atalakitas Newton-ra
            time.sleep(meresgyak)

            # Cache-be mentes meresenkent arra az esetre, ha megszakadna a kapcsolat a meroeszkozzel:
            mentcache(mereseredmeny, "cache_meres")
    #Teljes meres mentese cache-be
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
# Min, Max mar letezo fgv-k, fejlesztes kesobbi stadiumaban a kiertekelesi szempontok bovithetok

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

# DAG vegrehajto

mereseredmeny = cache_betoltes("cache_meres")

if mereseredmeny != None:
    (meresszam, meresgyak, hatarmin, hatarmax) = betoltcache("cache_bemenet")

if mereseredmeny == None:
    apivalaszt = str(input("Meres valodi meroeszkozzel (V) vagy szimulalt meres (S)? - V/S: ").upper())
    while apivalaszt not in ("V", "S"):
        kerdes = str(input("Nem megfelelo bemenet. Meres valodi meroeszkozzel (V) vagy szimulalt meres (S)? - V/S: ").upper())
        if kerdes == "V" or kerdes == "S":
            break

    if apivalaszt == "V":
        meresszam = int(input("Meresek szama: "))
        meresgyak = int(input("Meresek gyakorisaga (masodpercben!): "))
        hatarmin = 0.0001 * g
        hatarmax = 6.2 * g
        # hatarmin/hatarmax = eszkoz mereshatara * g = ... [Newton]
        mereseredmeny = valosmeres(meresszam, meresgyak)       
        mentcache((meresszam, meresgyak, hatarmin, hatarmax), "cache_bemenet")

    if apivalaszt == "S":
        meresszam = int(input("Szimulalt meresek szama: "))
        meresgyak = int(input("Szimulalt meresek gyakorisaga (masodpercben!): "))
        hatarmin = float(input("Meresi intervallum minimuma: "))
        hatarmax = float(input("Meresi intervallum maximuma: "))
        mereseredmeny = meres(meresszam, meresgyak, hatarmin, hatarmax)
        mentcache((meresszam, meresgyak, hatarmin, hatarmax), "cache_bemenet")

folytatas = ellenorzes(mereseredmeny, meresszam, hatarmin, hatarmax)

if folytatas == False:
    exit()

kiertekeles = {
    "Atlag": [atlag(mereseredmeny)],
    "Minimum": [min(mereseredmeny)],
    "Maximum": [max(mereseredmeny)]
}

exportalas(kiertekeles, "eredmeny")