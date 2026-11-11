import csv
import sqlite3
import tkinter as tk
from datetime import date, datetime
from tkinter import filedialog, messagebox, ttk


class EVKEszkozNyilvantarto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eszköznyilvántartó és karbantartási napló")
        self.geometry("850x700")

        self.kapcsolat = sqlite3.connect("eszkozok.db")
        self.kapcsolat.execute("PRAGMA foreign_keys = ON")

        self.evk_adatbazis_elokeszitese()
        self.evk_felulet_elkeszitese()
        self.evk_lista_frissitese()
        self.evk_karbantartas_lista_frissitese()

    def evk_adatbazis_elokeszitese(self):
        self.kapcsolat.execute(
            "CREATE TABLE IF NOT EXISTS eszkozok "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "nev TEXT NOT NULL, kategoria TEXT NOT NULL)"
        )
        self.kapcsolat.execute(
            "CREATE TABLE IF NOT EXISTS karbantartas "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "eszkoz_id INTEGER NOT NULL, datum TEXT NOT NULL, "
            "leiras TEXT NOT NULL, "
            "FOREIGN KEY (eszkoz_id) REFERENCES eszkozok(id) "
            "ON DELETE CASCADE)"
        )
        self.kapcsolat.commit()

    def evk_felulet_elkeszitese(self):
        eszkoz_frame = ttk.LabelFrame(self, text="Eszközök", padding=10)
        eszkoz_frame.pack(fill="both", expand=True, padx=10, pady=10)

        beviteli_sor = ttk.Frame(eszkoz_frame)
        beviteli_sor.pack(fill="x")

        ttk.Label(beviteli_sor, text="Eszköz neve:").grid(row=0, column=0)
        self.nev_mezo = ttk.Entry(beviteli_sor)
        self.nev_mezo.grid(row=0, column=1, padx=5)

        ttk.Label(beviteli_sor, text="Kategória:").grid(row=0, column=2)
        self.kategoria_mezo = ttk.Entry(beviteli_sor)
        self.kategoria_mezo.grid(row=0, column=3, padx=5)

        ttk.Button(
            beviteli_sor,
            text="Hozzáadás",
            command=self.evk_eszkoz_hozzaadas
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            beviteli_sor,
            text="Módosítás",
            command=self.evk_eszkoz_modositasa
        ).grid(row=1, column=4, pady=5)

        kereso_sor = ttk.Frame(eszkoz_frame)
        kereso_sor.pack(fill="x", pady=(5, 0))

        ttk.Label(kereso_sor, text="Keresés:").pack(side="left")
        self.kereso_mezo = ttk.Entry(kereso_sor)
        self.kereso_mezo.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )
        self.kereso_mezo.bind(
            "<Return>",
            self.evk_eszkoz_keresese
        )

        ttk.Button(
            kereso_sor,
            text="Keresés",
            command=self.evk_eszkoz_keresese
        ).pack(side="left", padx=5)

        ttk.Button(
            kereso_sor,
            text="Összes eszköz",
            command=self.evk_osszes_eszkoz
        ).pack(side="left")

        self.lista = ttk.Treeview(
            eszkoz_frame,
            columns=("id", "nev", "kategoria"),
            show="headings",
            height=6
        )
        self.lista.heading("id", text="Azonosító")
        self.lista.heading("nev", text="Eszköz neve")
        self.lista.heading("kategoria", text="Kategória")
        self.lista.bind(
            "<<TreeviewSelect>>",
            self.evk_kijelolt_eszkoz_betoltese
        )
        self.lista.pack(fill="both", expand=True, pady=10)

        ttk.Button(
            eszkoz_frame,
            text="Kijelölt eszköz törlése",
            command=self.evk_eszkoz_torlese
        ).pack()

        ttk.Button(
            eszkoz_frame,
            text="Eszközlista mentése CSV-fájlba",
            command=self.evk_eszkozok_exportalasa
        ).pack(pady=5)

        naplo_frame = ttk.LabelFrame(
            self,
            text="Karbantartási napló",
            padding=10
        )
        naplo_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        naplo_bevitel = ttk.Frame(naplo_frame)
        naplo_bevitel.pack(fill="x")

        ttk.Label(naplo_bevitel, text="Dátum (ÉÉÉÉ-HH-NN):").grid(
            row=0,
            column=0
        )
        self.datum_mezo = ttk.Entry(naplo_bevitel, width=14)
        self.datum_mezo.grid(row=0, column=1, padx=5)
        self.datum_mezo.insert(0, date.today().isoformat())

        ttk.Label(naplo_bevitel, text="Leírás:").grid(row=0, column=2)
        self.leiras_mezo = ttk.Entry(naplo_bevitel, width=35)
        self.leiras_mezo.grid(row=0, column=3, padx=5)

        ttk.Button(
            naplo_bevitel,
            text="Naplóbejegyzés hozzáadása",
            command=self.evk_karbantartas_hozzaadas
        ).grid(row=0, column=4, padx=5)

        karb_kereso_sor = ttk.Frame(naplo_frame)
        karb_kereso_sor.pack(fill="x", pady=(5, 0))

        ttk.Label(
            karb_kereso_sor,
            text="Napló keresése:"
        ).pack(side="left")

        self.karb_kereso_mezo = ttk.Entry(karb_kereso_sor)
        self.karb_kereso_mezo.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )
        self.karb_kereso_mezo.bind(
            "<Return>",
            self.evk_karbantartas_keresese
        )

        ttk.Button(
            karb_kereso_sor,
            text="Keresés",
            command=self.evk_karbantartas_keresese
        ).pack(side="left", padx=5)

        ttk.Button(
            karb_kereso_sor,
            text="Teljes napló",
            command=self.evk_teljes_karbantartasi_naplo
        ).pack(side="left")

        self.karb_lista = ttk.Treeview(
            naplo_frame,
            columns=("id", "datum", "eszkoz", "leiras"),
            show="headings",
            height=6
        )
        self.karb_lista.heading("id", text="Azonosító")
        self.karb_lista.heading("datum", text="Dátum")
        self.karb_lista.heading("eszkoz", text="Eszköz")
        self.karb_lista.heading("leiras", text="Karbantartás leírása")
        self.karb_lista.bind(
            "<<TreeviewSelect>>",
            self.evk_kijelolt_karbantartas_betoltese
        )
        self.karb_lista.pack(fill="both", expand=True, pady=10)

        ttk.Button(
            naplo_frame,
            text="Kijelölt naplóbejegyzés törlése",
            command=self.evk_karbantartas_torlese
        ).pack()

        ttk.Button(
            naplo_frame,
            text="Kijelölt naplóbejegyzés módosítása",
            command=self.evk_karbantartas_modositasa
        ).pack()

        ttk.Button(
            naplo_frame,
            text="Karbantartási napló mentése CSV-fájlba",
            command=self.evk_karbantartas_exportalasa
        ).pack()

    def evk_eszkoz_hozzaadas(self):
        nev = self.nev_mezo.get().strip()
        kategoria = self.kategoria_mezo.get().strip()

        if not nev or not kategoria:
            messagebox.showwarning(
                "Hiányzó adat",
                "Töltsd ki az eszköz nevét és kategóriáját!"
            )
            return

        self.kapcsolat.execute(
            "INSERT INTO eszkozok (nev, kategoria) VALUES (?, ?)",
            (nev, kategoria)
        )
        self.kapcsolat.commit()
        self.nev_mezo.delete(0, tk.END)
        self.kategoria_mezo.delete(0, tk.END)
        self.evk_lista_frissitese()

    def evk_eszkoz_keresese(self, event=None):
        kereses = self.kereso_mezo.get().strip()
        self.evk_lista_frissitese(kereses)

    def evk_osszes_eszkoz(self):
        self.kereso_mezo.delete(0, tk.END)
        self.evk_lista_frissitese()

    def evk_lista_frissitese(self, kereses=""):
        for sor in self.lista.get_children():
            self.lista.delete(sor)

        minta = f"%{kereses}%"
        eszkozok = self.kapcsolat.execute(
            "SELECT id, nev, kategoria FROM eszkozok "
            "WHERE nev LIKE ? OR kategoria LIKE ? "
            "ORDER BY nev",
            (minta, minta)
        ).fetchall()

        for eszkoz in eszkozok:
            self.lista.insert("", tk.END, values=eszkoz)

        self.evk_karbantartas_lista_frissitese()

    def evk_eszkoz_torlese(self):
        kijelolt = self.lista.selection()

        if not kijelolt:
            messagebox.showwarning(
                "Nincs kijelölés",
                "Előbb jelölj ki egy eszközt a listában!"
            )
            return

        eszkoz = self.lista.item(kijelolt[0], "values")
        biztos = messagebox.askyesno(
            "Törlés megerősítése",
            f"Biztosan törlöd ezt az eszközt: {eszkoz[1]}? "
            "A kapcsolódó naplóbejegyzések is törlődnek."
        )

        if biztos:
            self.kapcsolat.execute(
                "DELETE FROM eszkozok WHERE id = ?",
                (eszkoz[0],)
            )
            self.kapcsolat.commit()
            self.evk_lista_frissitese()

    def evk_karbantartas_hozzaadas(self):
        kijelolt = self.lista.selection()

        if not kijelolt:
            messagebox.showwarning(
                "Nincs kijelölés",
                "Jelöld ki azt az eszközt, amelyhez bejegyzést készítesz!"
            )
            return

        datum = self.datum_mezo.get().strip()
        leiras = self.leiras_mezo.get().strip()

        try:
            datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning(
                "Hibás dátum",
                "A dátum formátuma legyen ÉÉÉÉ-HH-NN, például 2026-11-09."
            )
            return

        if not leiras:
            messagebox.showwarning(
                "Hiányzó leírás",
                "Írd le röviden a karbantartás tartalmát!"
            )
            return

        eszkoz = self.lista.item(kijelolt[0], "values")
        self.kapcsolat.execute(
            "INSERT INTO karbantartas (eszkoz_id, datum, leiras) "
            "VALUES (?, ?, ?)",
            (eszkoz[0], datum, leiras)
        )
        self.kapcsolat.commit()
        self.leiras_mezo.delete(0, tk.END)
        self.evk_karbantartas_lista_frissitese()

    def evk_karbantartas_keresese(self, event=None):
        kereses = self.karb_kereso_mezo.get().strip()
        self.evk_karbantartas_lista_frissitese(kereses)

    def evk_teljes_karbantartasi_naplo(self):
        self.karb_kereso_mezo.delete(0, tk.END)
        self.evk_karbantartas_lista_frissitese("")

    def evk_karbantartas_lista_frissitese(self, kereses=None):
        for sor in self.karb_lista.get_children():
            self.karb_lista.delete(sor)

        if kereses is None:
            kereses = self.karb_kereso_mezo.get().strip()

        minta = f"%{kereses}%"
        bejegyzesek = self.kapcsolat.execute(
            "SELECT karbantartas.id, karbantartas.datum, "
            "eszkozok.nev, karbantartas.leiras "
            "FROM karbantartas "
            "JOIN eszkozok ON eszkozok.id = karbantartas.eszkoz_id "
            "WHERE karbantartas.datum LIKE ? "
            "OR eszkozok.nev LIKE ? "
            "OR karbantartas.leiras LIKE ? "
            "ORDER BY karbantartas.datum DESC",
            (minta, minta, minta)
        ).fetchall()

        for bejegyzes in bejegyzesek:
            self.karb_lista.insert("", tk.END, values=bejegyzes)

    def evk_karbantartas_torlese(self):
        kijelolt = self.karb_lista.selection()

        if not kijelolt:
            messagebox.showwarning(
                "Nincs kijelölés",
                "Előbb jelölj ki egy naplóbejegyzést!"
            )
            return

        bejegyzes = self.karb_lista.item(kijelolt[0], "values")
        biztos = messagebox.askyesno(
            "Törlés megerősítése",
            f"Biztosan törlöd a {bejegyzes[1]} dátumú "
            f"{bejegyzes[2]} eszközhöz tartozó bejegyzést?"
        )

        if biztos:
            self.kapcsolat.execute(
                "DELETE FROM karbantartas WHERE id = ?",
                (bejegyzes[0],)
            )
            self.kapcsolat.commit()
            self.evk_karbantartas_lista_frissitese()

    def evk_kijelolt_karbantartas_betoltese(self, event=None):
        kijelolt = self.karb_lista.selection()

        if kijelolt:
            bejegyzes = self.karb_lista.item(kijelolt[0], "values")
            self.datum_mezo.delete(0, tk.END)
            self.datum_mezo.insert(0, bejegyzes[1])
            self.leiras_mezo.delete(0, tk.END)
            self.leiras_mezo.insert(0, bejegyzes[3])

    def evk_karbantartas_modositasa(self):
        kijelolt = self.karb_lista.selection()

        if not kijelolt:
            messagebox.showwarning(
                "Nincs kijelölés",
                "Előbb jelölj ki egy naplóbejegyzést!"
            )
            return

        datum = self.datum_mezo.get().strip()
        leiras = self.leiras_mezo.get().strip()

        try:
            datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning(
                "Hibás dátum",
                "A dátum formátuma legyen ÉÉÉÉ-HH-NN, például 2026-11-09."
            )
            return

        if not leiras:
            messagebox.showwarning(
                "Hiányzó leírás",
                "Írd le röviden a karbantartás tartalmát!"
            )
            return

        bejegyzes = self.karb_lista.item(kijelolt[0], "values")
        self.kapcsolat.execute(
            "UPDATE karbantartas SET datum = ?, leiras = ? WHERE id = ?",
            (datum, leiras, bejegyzes[0])
        )
        self.kapcsolat.commit()
        self.evk_karbantartas_lista_frissitese()
        self.leiras_mezo.delete(0, tk.END)

    def evk_karbantartas_exportalasa(self):
        bejegyzesek = self.kapcsolat.execute(
            "SELECT karbantartas.datum, eszkozok.nev, "
            "karbantartas.leiras "
            "FROM karbantartas "
            "JOIN eszkozok ON eszkozok.id = karbantartas.eszkoz_id "
            "ORDER BY karbantartas.datum DESC"
        ).fetchall()

        if not bejegyzesek:
            messagebox.showwarning(
                "Nincs adat",
                "A karbantartási napló még üres."
            )
            return

        fajlnev = filedialog.asksaveasfilename(
            title="Karbantartási napló mentése",
            defaultextension=".csv",
            filetypes=[("CSV-fájl", "*.csv")]
        )

        if not fajlnev:
            return

        try:
            with open(
                fajlnev,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as fajl:
                iro = csv.writer(fajl, delimiter=";")
                iro.writerow(
                    ["Dátum", "Eszköz", "Karbantartás leírása"]
                )
                iro.writerows(bejegyzesek)
        except OSError as hiba:
            messagebox.showerror(
                "Mentési hiba",
                f"A fájl mentése nem sikerült: {hiba}"
            )
            return

        messagebox.showinfo(
            "Sikeres mentés",
            "A karbantartási napló CSV-fájlba került."
        )

    def evk_kijelolt_eszkoz_betoltese(self, event=None):
        kijelolt = self.lista.selection()

        if kijelolt:
            eszkoz = self.lista.item(kijelolt[0], "values")
            self.nev_mezo.delete(0, tk.END)
            self.nev_mezo.insert(0, eszkoz[1])
            self.kategoria_mezo.delete(0, tk.END)
            self.kategoria_mezo.insert(0, eszkoz[2])

    def evk_eszkoz_modositasa(self):
        kijelolt = self.lista.selection()

        if not kijelolt:
            messagebox.showwarning(
                "Nincs kijelölés",
                "Előbb jelölj ki egy eszközt a módosításhoz!"
            )
            return

        nev = self.nev_mezo.get().strip()
        kategoria = self.kategoria_mezo.get().strip()

        if not nev or not kategoria:
            messagebox.showwarning(
                "Hiányzó adat",
                "Az eszköz neve és kategóriája nem maradhat üresen!"
            )
            return

        eszkoz = self.lista.item(kijelolt[0], "values")
        self.kapcsolat.execute(
            "UPDATE eszkozok SET nev = ?, kategoria = ? WHERE id = ?",
            (nev, kategoria, eszkoz[0])
        )
        self.kapcsolat.commit()
        self.evk_lista_frissitese()
        self.nev_mezo.delete(0, tk.END)
        self.kategoria_mezo.delete(0, tk.END)

    def evk_eszkozok_exportalasa(self):
        eszkozok = self.kapcsolat.execute(
            "SELECT id, nev, kategoria FROM eszkozok ORDER BY nev"
        ).fetchall()

        if not eszkozok:
            messagebox.showwarning(
                "Nincs adat",
                "Az eszközlista még üres."
            )
            return

        fajlnev = filedialog.asksaveasfilename(
            title="Eszközlista mentése",
            initialfile="eszkozlista.csv",
            defaultextension=".csv",
            filetypes=[("CSV-fájl", "*.csv")]
        )

        if not fajlnev:
            return

        try:
            with open(
                fajlnev,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as fajl:
                iro = csv.writer(fajl, delimiter=";")
                iro.writerow(
                    ["Azonosító", "Eszköz neve", "Kategória"]
                )
                iro.writerows(eszkozok)
        except OSError as hiba:
            messagebox.showerror(
                "Mentési hiba",
                f"A fájl mentése nem sikerült: {hiba}"
            )
            return

        messagebox.showinfo(
            "Sikeres mentés",
            "Az eszközlista CSV-fájlba került."
        )