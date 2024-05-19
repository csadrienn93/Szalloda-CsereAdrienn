import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def ar_megad(self):
        pass

class Egy_ágyas_szoba(Szoba):
    def ar_megad(self):
        return self.ar

    def __init__(self, szobaszam):
        super().__init__(szobaszam, 15000)

class Két_ágyas_szoba(Szoba):
    def ar_megad(self):
        return self.ar

    def __init__(self, szobaszam):
        super().__init__(szobaszam, 30000)

class Franciaágyas_szoba_pótággyal(Szoba):
    def ar_megad(self):
        return self.ar

    def __init__(self, szobaszam):
        super().__init__(szobaszam, 20000)


class Foglalas:
    def __init__(self, szobaszam, datum, foglalasi_szam, ar):
        self.szobaszam = szobaszam
        self.datum = datum
        self.foglalasi_szam = foglalasi_szam
        self.ar = ar

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []
        self.szobak_hozzaadasa()

    def szobak_hozzaadasa(self):
        self.szobak.append(Egy_ágyas_szoba("101"))
        self.szobak.append(Két_ágyas_szoba("102"))
        self.szobak.append(Franciaágyas_szoba_pótággyal("103"))

    def foglalas(self, szobaszam, datum):
        szoba = next((s for s in self.szobak if s.szobaszam == szobaszam), None)
        if not szoba:
            return "Nem létező szobaszám."

        datum_obj = datetime.strptime(datum, '%Y-%m-%d')
        if datum_obj < datetime.now():
            return "A foglalási dátum nem lehet később, mint a mai dátum."

        if any(f.szobaszam == szobaszam and f.datum == datum for f in self.foglalasok):
            return "Ez a szoba a megadott időpontban már foglalt"

        foglalasi_szam = str(random.randint(100000, 999999))
        self.foglalasok.append(Foglalas(szobaszam, datum, foglalasi_szam, szoba.ar_megad()))
        return f"Foglalás sikeres. Foglalási szám: {foglalasi_szam}, Ár: {szoba.ar_megad()} Ft"

    def foglalasok_listazasa(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return "\n".join(
            f"Dátum: {f.datum}, Szobaszám: {f.szobaszam}, Foglalási szám: {f.foglalasi_szam}, Ár: {f.ar} Ft" for f in
            self.foglalasok)

    def foglalas_torlese(self, foglalasi_szam):
        torlendo_foglalas = next((f for f in self.foglalasok if f.foglalasi_szam == foglalasi_szam), None)
        if torlendo_foglalas:
            self.foglalasok.remove(torlendo_foglalas)
            return f"Foglalás törölve: {foglalasi_szam}"
        return "Ilyen foglalási szám nem létezik."


def kockacukor():
    szalloda = Szalloda("Kockacukor Hotel")
    print(f"Üdvözöljük a {szalloda.nev}**** foglalási felületén!\n"
          "A hotel személyzete kellemes kikapcsolódást és jó pihenést kíván Önnek/Önöknek!" )

    szalloda.foglalas("102", (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y.%m.%d'))
    szalloda.foglalas("103", (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y.%m.%d'))
    szalloda.foglalas("101", (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y.%m.%d'))
    szalloda.foglalas("102", (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y.%m.%d'))
    szalloda.foglalas("103", (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y.%m.%d'))

    while True:
        print("\n1. Szoba foglalás\n2. Jelenlegi foglalások listázása\n3. Foglalás törlése\n4. Kilépés")
        valasztas = input("Mit szeretne tenni: ")
        if valasztas == "1":
            while True:
                szobaszam = input("Adja meg a szobaszámot:\n (Egy_ágyas_szoba: 101\n Két_ágyas_szoba: 102\n Franciaágyas_szoba_pótággyal: 103): ")
                szoba = next((s for s in szalloda.szobak if s.szobaszam == szobaszam), None)
                if szoba:
                    break
                else:
                    print("Nem létező szobaszám.")
            datum = input("Adja meg a foglalás dátumát (YYYY.MM.DD): ")
            print(szalloda.foglalas(szobaszam, datum))
        elif valasztas == "2":
            print(szalloda.foglalasok_listazasa())
        elif valasztas == "3":
            foglalasi_szam = input("Adja meg a foglalás számát, amit törölni szeretne: ")
            print(szalloda.foglalas_torlese(foglalasi_szam))
        elif valasztas == "4":
            print("Kilépés a programból.")
            break
        else:
            print("Rossz menüpontot adott meg. Kérjük válasszon a felsorolt lehetőségek közül 1-től 4-ig.")

kockacukor()