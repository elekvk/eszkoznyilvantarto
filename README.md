# Eszköznyilvántartó és karbantartási napló

**Készítette:** Elek Viktória Krisztina – W2FOPY

## A program leírása

Az alkalmazással eszközöket lehet nyilvántartani, keresni, módosítani és törölni. A kiválasztott eszközökhöz dátummal és leírással karbantartási bejegyzéseket lehet rögzíteni, keresni, módosítani és törölni. Az eszközlista és a karbantartási napló az oszlopfejlécekre kattintva rendezhető, az újabb kattintás megfordítja a rendezés sorrendjét. Mindkét lista CSV-fájlba is menthető. Az adatokat SQLite-adatbázis tárolja.

## Futtatás

A program a `main.py` fájl elindításával futtatható.

## Programfelépítés

- `main.py` – létrehozza a `root` főablakot, elindítja az `app` alkalmazást, majd meghívja a főablak eseményciklusát.
- `root` – a Tkinter főablaka.
- `app` – az `EVKEszkozNyilvantarto` osztály példánya.

## Fájlok

- `main.py` – a program indítófájlja
- `evk_eszkozok.py` – a grafikus felületet és a program működését tartalmazó saját modul
- `eszkozok.db` – a program által létrehozott SQLite-adatbázis

## Használt modulok és függvények

### Tanult modul: `tkinter`

A grafikus felület és az eseménykezelés megvalósítására szolgál.

- `tk.Tk()` – létrehozza a főablakot
- `ttk.LabelFrame()`, `ttk.Frame()`, `ttk.Label()`, `ttk.Entry()`, `ttk.Button()` – felületi elemek létrehozása
- `ttk.Treeview()` – táblázatos listák megjelenítése
- `bind()` – események, például az Enter billentyű vagy a kijelölés kezelése
- `mainloop()` – elindítja a grafikus felület eseményciklusát

### Bemutatandó modul: `sqlite3`

Az SQLite-adatbázis kezelésére szolgál.

- `sqlite3.connect("eszkozok.db")` – kapcsolat létrehozása az adatbázissal
- `execute()` – SQL-parancs végrehajtása
- `commit()` – az adatbázis módosításainak mentése
- `fetchone()` – egy lekérdezési eredmény beolvasása
- `fetchall()` – a lekérdezési eredmények beolvasása

### További használt modulok

- `datetime` – dátum lekérése, ellenőrzése és átalakítása: `date.today()`, `datetime.strptime()`, `strftime()`, `isoformat()`
- `csv` – CSV-fájl készítése: `csv.writer()`, `writerow()`, `writerows()`
- `filedialog` – a mentési hely kiválasztása: `asksaveasfilename()`
- `messagebox` – figyelmeztetések, megerősítések és visszajelzések megjelenítése: `showwarning()`, `askyesno()`, `showerror()`, `showinfo()`

## Saját modul, osztály és függvények

Saját modul: `evk_eszkozok.py`

Saját osztály: `EVKEszkozNyilvantarto`

Fontosabb saját metódusok: `evk_adatbazis_elokeszitese`, `evk_felulet_elkeszitese`, `evk_datum_atalakitasa`, `evk_eszkoz_hozzaadas`, `evk_eszkoz_keresese`, `evk_osszes_eszkoz`, `evk_eszkoz_db_frissitese`, `evk_lista_frissitese`, `evk_eszkoz_lista_rendezese`, `evk_eszkoz_torlese`, `evk_eszkoz_modositasa`, `evk_karbantartas_hozzaadas`, `evk_karbantartas_keresese`, `evk_teljes_karbantartasi_naplo`, `evk_karbantartas_lista_frissitese`, `evk_karbantartasi_lista_rendezese`, `evk_karbantartas_torlese`, `evk_kijelolt_karbantartas_betoltese`, `evk_karbantartas_modositasa`, `evk_karbantartas_exportalasa`, `evk_eszkozok_exportalasa`, `evk_ablak_bezarasa`.

A saját metódusok neve az `evk` monogrammal kezdődik.