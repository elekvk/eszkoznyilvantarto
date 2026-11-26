# Eszköznyilvántartó és karbantartási napló

**Készítette:** Elek Viktória Krisztina – W2FOPY

## A program leírása

Az alkalmazás eszközök és a hozzájuk tartozó karbantartási bejegyzések nyilvántartására szolgál. Az eszközöket és a naplóbejegyzéseket hozzá lehet adni, keresni, módosítani és törölni. Az eszközlista és a karbantartási napló CSV-fájlba exportálható.

A grafikus felületen külön oldalon található a kezdőlap, az eszközök kezelése és a karbantartási napló. A kezdőlapon látható az eszközök és a naplóbejegyzések száma, valamint a legutóbbi karbantartás dátuma. Az adatokat SQLite-adatbázis tárolja. A dátum ponttal és záró pont nélkül is megadható, például `2026.11.19.` vagy `2026.11.19`.

## Futtatás

A program a `main.py` fájl elindításával futtatható. PyCharmban a `main.py` fájlt kell megnyitni és elindítani.

A program Python beépített modulokat használ, külön csomag telepítése nem szükséges.

## Programfelépítés

- `main.py` létrehozza a Tkinter főablakot, példányosítja az `EVKEszkozNyilvantarto` osztályt, majd elindítja az eseményciklust.
- `root` a Tkinter főablaka.
- `app` az `EVKEszkozNyilvantarto` osztály példánya.

## Fájlok és mappák

- `main.py` – a program indítófájlja
- `evk_eszkozok.py` – a grafikus felületet és a program működését tartalmazó saját modul
- `eszkozok.db` – a program futásakor létrejövő SQLite-adatbázis
- `mintakimenetek/eszkozlista.csv` – az eszközlista exportált mintafájlja
- `mintakimenetek/karbantartasi_naplo.csv` – a karbantartási napló exportált mintafájlja
- `.gitignore` – a Git számára kihagyandó fájlok és mappák felsorolása
- `README.md` – a program leírása és dokumentációja

## Használt modulok és függvények

### Tanult modul: `tkinter`

A grafikus felület és az eseménykezelés megvalósítására szolgál.

- `tk.Tk()` – létrehozza a főablakot
- `ttk.Frame()`, `ttk.LabelFrame()`, `ttk.Label()`, `ttk.Entry()` és `ttk.Button()` – felületi elemek létrehozása
- `ttk.Notebook()` – külön oldalak létrehozása
- `ttk.Treeview()` – az eszközök és a naplóbejegyzések táblázatos megjelenítése
- `bind()` – billentyűzet- és kijelölési események kezelése
- `mainloop()` – elindítja a grafikus felület eseményciklusát

### Bemutatandó modul: `sqlite3`

Az SQLite-adatbázis kezelésére szolgál. A program a modul függvényét, valamint az adatbázis-kapcsolat és a kurzor metódusait használja.

- `sqlite3.connect("eszkozok.db")` – kapcsolat létrehozása az adatbázissal
- `Connection.execute(...)` – SQL-parancs végrehajtása
- `Connection.commit()` – az adatbázis-módosítások mentése
- `Cursor.fetchone()` – egy lekérdezési eredmény beolvasása
- `Cursor.fetchall()` – a lekérdezési eredmények beolvasása

### További használt modulok

- `datetime` – dátum lekérése, ellenőrzése és átalakítása: `date.today()`, `datetime.strptime()`, `strftime()`, `isoformat()`
- `csv` – CSV-fájl készítése: `csv.writer()`, `writerow()`, `writerows()`
- `filedialog` – mentési ablak megnyitása: `asksaveasfilename()`
- `messagebox` – figyelmeztetések, megerősítések és visszajelzések megjelenítése: `showwarning()`, `askyesno()`, `showerror()`, `showinfo()`
- `pathlib` – a projektmappa meghatározása és a `mintakimenetek` mappa létrehozása: `Path(__file__).resolve().parent`, `mkdir()`

## Saját modul, osztály és metódusok

**Saját modul:** `evk_eszkozok.py`

**Saját osztály:** `EVKEszkozNyilvantarto`

**Fontosabb saját metódusok:**

`evk_adatbazis_elokeszitese`, `evk_felulet_elkeszitese`, `evk_datum_atalakitasa`, `evk_eszkoz_hozzaadas`, `evk_eszkoz_keresese`, `evk_osszes_eszkoz`, `evk_eszkoz_db_frissitese`, `evk_lista_frissitese`, `evk_eszkoz_torlese`, `evk_karbantartas_hozzaadas`, `evk_karbantartas_keresese`, `evk_teljes_karbantartasi_naplo`, `evk_karbantartas_lista_frissitese`, `evk_kezdolap_statisztika_frissitese`, `evk_eszkoz_lista_rendezese`, `evk_karbantartasi_lista_rendezese`, `evk_karbantartas_torlese`, `evk_kijelolt_karbantartas_betoltese`, `evk_karbantartas_modositasa`, `evk_kijelolt_eszkoz_betoltese`, `evk_eszkoz_modositasa`, `evk_eszkozok_exportalasa`, `evk_karbantartas_exportalasa`, `evk_ablak_bezarasa`.

A saját modul, osztály és metódusok nevében szerepel a készítő `EVK` monogramja.