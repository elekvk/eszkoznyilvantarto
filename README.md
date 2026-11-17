# Eszköznyilvántartó és karbantartási napló

**Készítette:** Elek Viktória Krisztina - W2FOPY

## A program leírása

Az alkalmazással eszközöket lehet nyilvántartani, valamint a kiválasztott eszközökhöz dátummal és leírással karbantartási bejegyzéseket lehet rögzíteni. Az adatokat SQLite-adatbázis tárolja.

## Futtatás

A program a `main.py` fájl elindításával futtatható.

## Fájlok

- `main.py` – a program indítófájlja
- `evk_eszkozok.py` – a grafikus felület és a program működése
- `eszkozok.db` – a program által létrehozott adatbázis

## Használt modulok

- Tanult modul: `tkinter` – grafikus felület és eseménykezelés (`ttk`, `messagebox`)
- Bemutatandó modul: `sqlite3` – az adatbázis kezelése
  - `sqlite3.connect("eszkozok.db")` – kapcsolat létrehozása
  - `self.kapcsolat.execute(...)` – SQL-parancs végrehajtása
  - `self.kapcsolat.commit()` – módosítások mentése
  - `.fetchall()` – lekérdezési eredmények beolvasása
- Saját modul: `evk_eszkozok.py` – a program osztályát és saját metódusait tartalmazza
- `datetime` – dátum lekérése és ellenőrzése
- `csv` és `filedialog` – adatok CSV-fájlba mentése és a fájl helyének kiválasztása

## Saját osztály és függvények

Saját osztály: `EVKEszkozNyilvantarto`

Fontosabb saját metódusok: `evk_eszkoz_hozzaadas`, `evk_eszkoz_torlese`, `evk_karbantartas_hozzaadas`, `evk_lista_frissitese`.