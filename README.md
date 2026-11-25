# Eszköznyilvántartó és karbantartási napló

**Készítette:** Elek Viktória Krisztina – W2FOPY

## A program leírása

Az alkalmazással eszközöket lehet nyilvántartani, keresni, módosítani és törölni. A kiválasztott eszközökhöz dátummal és leírással karbantartási bejegyzéseket lehet rögzíteni, keresni, módosítani és törölni. Az eszközlista és a karbantartási napló az oszlopfejlécekre kattintva rendezhető, és CSV-fájlba menthető. Az adatokat SQLite-adatbázis tárolja.

A grafikus felület Kezdőlapból, Eszközök és Karbantartási napló fülekből áll. A két lista külön oldalon jelenik meg, saját görgetősávval.

## Futtatás

A program a `main.py` fájl elindításával futtatható.

## Programfelépítés

- `main.py` – létrehozza a `root` főablakot, elindítja az `app` alkalmazást, majd meghívja a főablak eseményciklusát.
- `root` – a Tkinter főablaka, amely a füleket tartalmazza.
- `app` – az `EVKEszkozNyilvantarto` osztály példánya.
- `Kezdőlap` – innen nyitható meg az eszközök vagy a karbantartási napló oldala.
- `Eszközök` – az eszközök kezelése, keresése, rendezése és CSV-exportja.
- `Karbantartási napló` – a bejegyzések kezelése, keresése, rendezése és CSV-exportja.

## Fájlok

- `main.py` – a program indítófájlja
- `evk_eszkozok.py` – a grafikus felületet és a program működését tartalmazó saját modul
- `eszkozok.db` – a program által létrehozott SQLite-adatbázis

## Használt modulok és függvények

### Tanult modul: `tkinter`

A grafikus felület és az eseménykezelés megvalósítására szolgál.

- `tk.Tk()` – létrehozza a főablakot
- `ttk.Notebook()` – füles oldalakat hoz létre
- `ttk.LabelFrame()`, `ttk.Frame()`, `ttk.Label()`, `ttk.Entry()`, `ttk.Button()` – felületi elemek létrehozása
- `ttk.Treeview()` – táblázatos listák megjelenítése
- `ttk.Scrollbar()` – a listák görgetése
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

Fontosabb saját metódusok: `evk_adatbazis_elokeszitese`, `evk_stilus_beallitasa`, `evk_felulet_elkeszitese`, `evk_datum_atalakitasa`, `evk_eszkoz_hozzaadas`, `evk_eszkoz_keresese`, `evk_osszes_eszkoz`, `evk_eszkoz_db_frissitese`, `evk_lista_frissitese`, `evk_eszkoz_lista_rendezese`, `evk_eszkoz_torlese`, `evk_eszkoz_modositasa`, `evk_karbantartas_hozzaadas`, `evk_karbantartas_keresese`, `evk_teljes_karbantartasi_naplo`, `evk_karbantartas_lista_frissitese`, `evk_karbantartasi_lista_rendezese`, `evk_karbantarta