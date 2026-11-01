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

- `tkinter`, `ttk`, `messagebox` – grafikus felület és eseménykezelés
- `sqlite3` – adatbázis-kezelés (`connect`, `execute`, `commit`, `fetchall`)
- `datetime` – dátum kezelése és ellenőrzése

## Saját osztály és függvények

Saját osztály: `EVKEszkozNyilvantarto`

Fontosabb saját metódusok: `evk_eszkoz_hozzaadas`, `evk_eszkoz_torlese`, `evk_karbantartas_hozzaadas`, `evk_lista_frissitese`.