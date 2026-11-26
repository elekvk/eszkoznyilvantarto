# Eszköznyilvántartó és karbantartási napló

**Készítette:** Elek Viktória Krisztina – W2FOPY

## A program leírása

Az alkalmazás eszközök és a hozzájuk kapcsolódó karbantartási bejegyzések nyilvántartására szolgál. Az eszközöket és a naplóbejegyzéseket hozzá lehet adni, keresni, módosítani és törölni. A listák oszlopfejléceire kattintva az adatok rendezhetők, az eszközlista és a karbantartási napló pedig CSV-fájlba exportálható.

A kezdőlapon látható az eszközök és a naplóbejegyzések száma, valamint a legutóbbi karbantartás dátuma. A dátum `ÉÉÉÉ.HH.NN.` vagy `ÉÉÉÉ.HH.NN` formában is megadható. Az adatokat SQLite-adatbázis tárolja.

## Futtatás

A program a `main.py` fájl elindításával futtatható.

## Programfelépítés

- `main.py` létrehozza a Tkinter `root` főablakot, példányosítja az `app` alkalmazást, majd elindítja a főablak eseményciklusát.
- `root` a Tkinter főablaka.
- `app` az `EVKEszkozNyilvantarto` osztály példánya.

## Fájlok

- `main.py` – a program indítófájlja
- `evk_eszkozok.py` – a grafikus felületet és a program működését tartalmazó saját modul
- `eszkozok.db` – az alkalmazás által létrehozott SQLite-adatbázis
- `README.md` – a program leírása és dokumentációja

## Használt modulok és függvények

### Tanult modul: `tkinter`

A grafikus felület és az eseménykezelés megvalósítására szolgál.

- `tk.Tk()` – létrehozza a főablakot
- `ttk.Frame()`, `ttk.LabelFrame()`, `ttk.Label()`, `ttk.Entry()` és `ttk.Button()` – felületi elemek létrehozása
- `ttk.Notebook()` – külön oldalakat hoz létre a kezdőlap, az eszközök és a karbantartási napló számára
- `ttk.Treeview()` – az eszközök és a naplóbejegyzések táblázatos megjelenítése
- `bind()` – billentyűzet- és kijelölési események kezelése
- `mainloop()` – elindítja a grafikus felület eseményciklusát

### Bemutatandó modul: `sqlite3`

Az SQLite-adatbázis kezelésére szolgál. A program a modul függvényét és az adatbázis-kapcsolat metódusait használja.

- `sqlite3.connect("eszkozok.db")` – kapcsolat létrehozása az adatbázissal
- `self.kapcsolat.execute(...)` – SQL-parancs végrehajtása
- `self.kapcsolat.commit()` – az adatbázis módosításainak mentése
- `.fetchone()` – egy lekérdezési eredmény beolvasása
- `.fetchall()` – a lekérdezési eredmények beolvasása

### További használt modulok

- `datetime` – dátum lekérése, ellenőrzése és átalakítása: `date.today()`, `datetime.strptime()`, `strftime()`, `isoformat()`
- `csv` – CSV-fájl készítése: `csv.writer()`, `writerow()`, `writerows()`
- `filedialog` – a mentési hely kiválasztása: `asksaveasfilename()`
- `messagebox` – figyelmeztetések, megerősítések és visszajelzések megjelenítése: `showwarning()`, `askyesno()`, `showerror()`, `showinfo()`

## Saját modul, osztály és metódusok

**Saját modul:** `evk_eszkozok.py`

**Saját osztály:** `EVKEszkozNyilvantarto`

**Fontosabb saját metódusok:**

`evk_adatbazis_elokeszitese`, `evk_felulet_elkeszitese`, `evk_datum_atalakitasa`, `evk_eszkoz_hozzaadas`, `evk_eszkoz_keresese`, `evk_osszes_eszkoz`, `evk_eszkoz_db_frissitese`, `evk_lista_frissitese`, `evk_eszkoz_torlese`, `evk_eszkoz_modositasa`, `evk_eszkoz_lista_rendezese`, `evk_karbantartas_hozzaadas`, `evk_karbantartas_keresese`, `evk_teljes_karbantartasi_naplo`, `evk_karbantartas_lista_frissitese`, `evk_kezdolap_statisztika_frissitese`, `evk_karbantartas_torlese`, `evk_karbantartas_modositasa`, `evk_karbantartasi_lista_rendezese`, `evk_eszkozok_exportalasa`, `evk_karbantartas_exportalasa`, `evk_ablak_bezarasa`.

A saját modul, osztály és metódusok nevében szerepel a készítő `EVK` monogramja.