import csv
import sqlite3
import tkinter as tk
from datetime import date, datetime
from tkinter import filedialog, messagebox, ttk
from pathlib import Path


class EVKEszkozNyilvantarto:
    def __init__(self, root):
        self.root = root
        self.root.title("Eszköznyilvántartó és karbantartási napló")
        self.root.geometry("1100x850")
        self.root.minsize(900, 700)
        self.root.protocol("WM_DELETE_WINDOW", self.evk_ablak_bezarasa)
        self.evk_stilus_beallitasa()

        self.kapcsolat = sqlite3.connect("eszkozok.db")
        self.kapcsolat.execute("PRAGMA foreign_keys = ON")

        self.evk_adatbazis_elokeszitese()
        self.evk_felulet_elkeszitese()
        self.evk_lista_frissitese()

    def evk_stilus_beallitasa(self):
        stilus = ttk.Style(self.root)
        if "clam" in stilus.theme_names():
            stilus.theme_use("clam")

        self.root.configure(bg="#F3F6F3")
        stilus.configure(".", font=("Segoe UI", 10))
        stilus.configure("TFrame", background="#F3F6F3")
        stilus.configure(
            "TLabel",
            background="#F3F6F3",
            foreground="#26332B"
        )
        stilus.configure(
            "TLabelframe",
            background="#FFFFFF",
            bordercolor="#DCE5DE",
            borderwidth=1,
            relief="solid"
        )
        stilus.configure(
            "TLabelframe.Label",
            background="#FFFFFF",
            foreground="#277A55",
            font=("Segoe UI", 11, "bold")
        )
        stilus.configure(
            "TEntry",
            padding=7,
            fieldbackground="#FFFFFF",
            foreground="#26332B",
            bordercolor="#D4DED6",
            lightcolor="#D4DED6",
            darkcolor="#D4DED6"
        )
        stilus.map(
            "TEntry",
            bordercolor=[("focus", "#4B9B70")],
            lightcolor=[("focus", "#4B9B70")],
            darkcolor=[("focus", "#4B9B70")]
        )
        stilus.configure("TNotebook", background="#F3F6F3", borderwidth=0)
        stilus.configure(
            "TNotebook.Tab",
            padding=(18, 10),
            font=("Segoe UI", 10, "bold"),
            background="#E8EEE9",
            foreground="#526158"
        )
        stilus.map(
            "TNotebook.Tab",
            background=[
                ("selected", "#FFFFFF"),
                ("active", "#DFEAE1")
            ],
            foreground=[
                ("selected", "#277A55"),
                ("active", "#26332B")
            ]
        )
        stilus.configure(
            "Header.TFrame",
            background="#FFFFFF"
        )
        stilus.configure(
            "HeaderTitle.TLabel",
            background="#FFFFFF",
            foreground="#20352A",
            font=("Segoe UI", 19, "bold")
        )
        stilus.configure(
            "HeaderSubtitle.TLabel",
            background="#FFFFFF",
            foreground="#6A786F",
            font=("Segoe UI", 10)
        )
        stilus.configure(
            "Welcome.TFrame",
            background="#FFFFFF",
            bordercolor="#DCE5DE",
            relief="solid",
            borderwidth=1
        )
        stilus.configure(
            "HomeTitle.TLabel",
            background="#FFFFFF",
            foreground="#20352A",
            font=("Segoe UI", 23, "bold")
        )
        stilus.configure(
            "HomeText.TLabel",
            background="#FFFFFF",
            foreground="#69776E",
            font=("Segoe UI", 11)
        )
        stilus.configure(
            "Card.TFrame",
            background="#FFFFFF",
            bordercolor="#DCE5DE",
            relief="solid",
            borderwidth=1
        )
        stilus.configure(
            "CardTitle.TLabel",
            background="#FFFFFF",
            foreground="#26332B",
            font=("Segoe UI", 14, "bold")
        )
        stilus.configure(
            "CardText.TLabel",
            background="#FFFFFF",
            foreground="#69776E",
            font=("Segoe UI", 10)
        )
        stilus.configure(
            "StatCaption.TLabel",
            background="#FFFFFF",
            foreground="#69776E",
            font=("Segoe UI", 9, "bold")
        )
        stilus.configure(
            "StatValue.TLabel",
            background="#FFFFFF",
            foreground="#277A55",
            font=("Segoe UI", 22, "bold")
        )
        stilus.configure(
            "Accent.TButton",
            background="#277A55",
            foreground="#FFFFFF",
            padding=(16, 10),
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        stilus.map(
            "Accent.TButton",
            background=[
                ("active", "#206746"),
                ("pressed", "#19563A")
            ],
            foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")]
        )
        stilus.configure(
            "TButton",
            background="#E8EEE9",
            foreground="#304137",
            padding=(11, 8),
            font=("Segoe UI", 9, "bold"),
            borderwidth=0
        )
        stilus.map(
            "TButton",
            background=[("active", "#DCE8DE"), ("pressed", "#D1DFD4")],
            foreground=[("active", "#20352A"), ("pressed", "#20352A")]
        )
        stilus.configure(
            "Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#2D3931",
            rowheight=30,
            font=("Segoe UI", 10),
            bordercolor="#DCE5DE"
        )
        stilus.configure(
            "Treeview.Heading",
            background="#E8EEE9",
            foreground="#34483A",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(8, 8)
        )
        stilus.map(
            "Treeview.Heading",
            background=[("active", "#DCE8DE")]
        )
        stilus.map(
            "Treeview",
            background=[("selected", "#277A55")],
            foreground=[("selected", "#FFFFFF")]
        )

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
        fejlec = ttk.Frame(self.root, style="Header.TFrame", padding=(24, 16))
        fejlec.pack(fill="x", padx=14, pady=(14, 0))
        ttk.Label(
            fejlec,
            text="Eszköznyilvántartó",
            style="HeaderTitle.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            fejlec,
            text="Eszközök és karbantartási előzmények egy helyen",
            style="HeaderSubtitle.TLabel"
        ).pack(anchor="w", pady=(3, 0))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=14)

        self.kezdolap_oldal = ttk.Frame(self.notebook)
        self.eszkoz_oldal = ttk.Frame(self.notebook)
        self.naplo_oldal = ttk.Frame(self.notebook)

        self.notebook.add(self.kezdolap_oldal, text="Kezdőlap")
        self.notebook.add(self.eszkoz_oldal, text="Eszközök")
        self.notebook.add(self.naplo_oldal, text="Karbantartási napló")

        kezdo_tartalom = ttk.Frame(self.kezdolap_oldal, padding=24)
        kezdo_tartalom.pack(fill="both", expand=True)

        udvozlo = ttk.Frame(
            kezdo_tartalom,
            padding=(30, 26),
            style="Welcome.TFrame"
        )
        udvozlo.pack(fill="x", pady=(0, 18))
        ttk.Label(
            udvozlo,
            text="Üdvözlünk!",
            style="HomeTitle.TLabel"
        ).pack(anchor="w", pady=(0, 8))
        ttk.Label(
            udvozlo,
            text=(
                "Itt kezelheted a nyilvántartott eszközöket és "
                "a hozzájuk tartozó karbantartási bejegyzéseket."
            ),
            style="HomeText.TLabel",
            wraplength=760,
            justify="left"
        ).pack(anchor="w")

        statisztikak = ttk.Frame(kezdo_tartalom)
        statisztikak.pack(fill="x", pady=(0, 22))
        for oszlop in range(3):
            statisztikak.columnconfigure(oszlop, weight=1)

        eszkoz_stat = ttk.Frame(
            statisztikak,
            style="Card.TFrame",
            padding=(18, 15)
        )
        eszkoz_stat.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(
            eszkoz_stat,
            text="NYILVÁNTARTOTT ESZKÖZÖK",
            style="StatCaption.TLabel"
        ).pack(anchor="w")
        self.kezdolap_eszkoz_szam = ttk.Label(
            eszkoz_stat,
            text="0",
            style="StatValue.TLabel"
        )
        self.kezdolap_eszkoz_szam.pack(anchor="w", pady=(4, 0))

        naplo_stat = ttk.Frame(
            statisztikak,
            style="Card.TFrame",
            padding=(18, 15)
        )
        naplo_stat.grid(row=0, column=1, sticky="nsew", padx=8)
        ttk.Label(
            naplo_stat,
            text="NAPLÓBEJEGYZÉSEK",
            style="StatCaption.TLabel"
        ).pack(anchor="w")
        self.kezdolap_naplo_szam = ttk.Label(
            naplo_stat,
            text="0",
            style="StatValue.TLabel"
        )
        self.kezdolap_naplo_szam.pack(anchor="w", pady=(4, 0))

        utolso_stat = ttk.Frame(
            statisztikak,
            style="Card.TFrame",
            padding=(18, 15)
        )
        utolso_stat.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        ttk.Label(
            utolso_stat,
            text="LEGUTÓBBI KARBANTARTÁS",
            style="StatCaption.TLabel"
        ).pack(anchor="w")
        self.kezdolap_utolso_datum = ttk.Label(
            utolso_stat,
            text="Nincs adat",
            style="CardTitle.TLabel"
        )
        self.kezdolap_utolso_datum.pack(anchor="w", pady=(8, 0))

        ttk.Label(
            kezdo_tartalom,
            text="Gyors elérés",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        gyors_eleres = ttk.Frame(kezdo_tartalom)
        gyors_eleres.pack(fill="x")
        gyors_eleres.columnconfigure(0, weight=1)
        gyors_eleres.columnconfigure(1, weight=1)

        eszkoz_kartya = ttk.Frame(
            gyors_eleres,
            style="Card.TFrame",
            padding=20
        )
        eszkoz_kartya.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(
            eszkoz_kartya,
            text="Eszközök",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 6))
        ttk.Label(
            eszkoz_kartya,
            text="Eszközök felvétele, keresése, módosítása és törlése.",
            style="CardText.TLabel",
            wraplength=360,
            justify="left"
        ).pack(anchor="w", pady=(0, 16))
        ttk.Button(
            eszkoz_kartya,
            text="Eszközök megnyitása",
            command=lambda: self.notebook.select(self.eszkoz_oldal),
            style="Accent.TButton"
        ).pack(anchor="w")

        naplo_kartya = ttk.Frame(
            gyors_eleres,
            style="Card.TFrame",
            padding=20
        )
        naplo_kartya.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        ttk.Label(
            naplo_kartya,
            text="Karbantartási napló",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 6))
        ttk.Label(
            naplo_kartya,
            text="Karbantartások rögzítése, keresése és exportálása.",
            style="CardText.TLabel",
            wraplength=360,
            justify="left"
        ).pack(anchor="w", pady=(0, 16))
        ttk.Button(
            naplo_kartya,
            text="Napló megnyitása",
            command=lambda: self.notebook.select(self.naplo_oldal),
            style="Accent.TButton"
        ).pack(anchor="w")

        eszkoz_frame = ttk.LabelFrame(
            self.eszkoz_oldal,
            text="Eszközök kezelése",
            padding=14
        )
        eszkoz_frame.pack(fill="both", expand=True, padx=14, pady=14)

        beviteli_sor = ttk.Frame(eszkoz_frame)
        beviteli_sor.pack(fill="x")
        beviteli_sor.columnconfigure(1, weight=1)
        beviteli_sor.columnconfigure(3, weight=1)

        ttk.Label(beviteli_sor, text="Eszköz neve:").grid(row=0, column=0)
        self.nev_mezo = ttk.Entry(beviteli_sor)
        self.nev_mezo.grid(row=0, column=1, padx=5, sticky="ew")

        ttk.Label(beviteli_sor, text="Kategória:").grid(row=0, column=2)
        self.kategoria_mezo = ttk.Entry(beviteli_sor)
        self.kategoria_mezo.grid(row=0, column=3, padx=5, sticky="ew")

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
        kereso_sor.pack(fill="x", pady=(12, 0))
        ttk.Label(kereso_sor, text="Keresés:").pack(side="left")
        self.kereso_mezo = ttk.Entry(kereso_sor)
        self.kereso_mezo.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8
        )
        self.kereso_mezo.bind("<Return>", self.evk_eszkoz_keresese)
        ttk.Button(
            kereso_sor,
            text="Keresés",
            command=self.evk_eszkoz_keresese
        ).pack(side="left", padx=4)
        ttk.Button(
            kereso_sor,
            text="Összes eszköz",
            command=self.evk_osszes_eszkoz
        ).pack(side="left", padx=(4, 0))

        self.ossz_eszkoz_cimke = ttk.Label(
            eszkoz_frame,
            text="Nyilvántartott eszközök száma: 0"
        )
        self.ossz_eszkoz_cimke.pack(anchor="w", pady=(12, 0))

        lista_frame = ttk.Frame(eszkoz_frame)
        lista_frame.pack(fill="both", expand=True, pady=10)

        self.lista = ttk.Treeview(
            lista_frame,
            columns=("id", "nev", "kategoria"),
            show="headings",
            height=6
        )
        self.lista.tag_configure("paros", background="#F2F6F2")
        self.lista.tag_configure("paratlan", background="#FFFFFF")
        self.lista.heading(
            "id",
            text="Azonosító",
            command=lambda: self.evk_eszkoz_lista_rendezese("id")
        )
        self.lista.heading(
            "nev",
            text="Eszköz neve",
            command=lambda: self.evk_eszkoz_lista_rendezese("nev")
        )
        self.lista.heading(
            "kategoria",
            text="Kategória",
            command=lambda: self.evk_eszkoz_lista_rendezese("kategoria")
        )
        self.lista.bind("<<TreeviewSelect>>", self.evk_kijelolt_eszkoz_betoltese)
        lista_scrollbar = ttk.Scrollbar(
            lista_frame,
            orient="vertical",
            command=self.lista.yview
        )
        self.lista.configure(yscrollcommand=lista_scrollbar.set)
        self.lista.pack(side="left", fill="both", expand=True)
        lista_scrollbar.pack(side="right", fill="y")

        eszkoz_muveletek = ttk.Frame(eszkoz_frame)
        eszkoz_muveletek.pack(fill="x", pady=(4, 0))
        ttk.Button(
            eszkoz_muveletek,
            text="Kijelölt eszköz törlése",
            command=self.evk_eszkoz_torlese
        ).pack(side="left", padx=(0, 8), pady=4)
        ttk.Button(
            eszkoz_muveletek,
            text="Eszközlista mentése CSV-fájlba",
            command=self.evk_eszkozok_exportalasa
        ).pack(side="left", padx=8, pady=4)

        naplo_frame = ttk.LabelFrame(
            self.naplo_oldal,
            text="Karbantartási napló kezelése",
            padding=14
        )
        naplo_frame.pack(fill="both", expand=True, padx=14, pady=14)

        naplo_bevitel = ttk.Frame(naplo_frame)
        naplo_bevitel.pack(fill="x")
        naplo_bevitel.columnconfigure(3, weight=1)

        ttk.Label(naplo_bevitel, text="Dátum (ÉÉÉÉ.HH.NN.):").grid(
            row=0,
            column=0
        )
        self.datum_mezo = ttk.Entry(naplo_bevitel, width=14)
        self.datum_mezo.grid(row=0, column=1, padx=5)
        self.datum_mezo.insert(0, date.today().strftime("%Y.%m.%d."))

        ttk.Label(naplo_bevitel, text="Leírás:").grid(row=0, column=2)
        self.leiras_mezo = ttk.Entry(naplo_bevitel, width=35)
        self.leiras_mezo.grid(row=0, column=3, padx=5, sticky="ew")

        ttk.Button(
            naplo_bevitel,
            text="Naplóbejegyzés hozzáadása",
            command=self.evk_karbantartas_hozzaadas
        ).grid(row=0, column=4, padx=5)

        karb_kereso_sor = ttk.Frame(naplo_frame)
        karb_kereso_sor.pack(fill="x", pady=(12, 0))
        ttk.Label(karb_kereso_sor, text="Napló keresése:").pack(side="left")
        self.karb_kereso_mezo = ttk.Entry(karb_kereso_sor)
        self.karb_kereso_mezo.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8
        )
        self.karb_kereso_mezo.bind(
            "<Return>",
            self.evk_karbantartas_keresese
        )
        ttk.Button(
            karb_kereso_sor,
            text="Keresés",
            command=self.evk_karbantartas_keresese
        ).pack(side="left", padx=4)
        ttk.Button(
            karb_kereso_sor,
            text="Teljes napló",
            command=self.evk_teljes_karbantartasi_naplo
        ).pack(side="left", padx=(4, 0))

        self.karb_db_cimke = ttk.Label(
            naplo_frame,
            text="Megjelenített naplóbejegyzések száma: 0"
        )
        self.karb_db_cimke.pack(anchor="w", pady=(12, 0))

        karb_lista_frame = ttk.Frame(naplo_frame)
        karb_lista_frame.pack(fill="both", expand=True, pady=10)

        self.karb_lista = ttk.Treeview(
            karb_lista_frame,
            columns=("id", "datum", "eszkoz", "leiras"),
            show="headings",
            height=6
        )
        self.karb_lista.tag_configure("paros", background="#F2F6F2")
        self.karb_lista.tag_configure("paratlan", background="#FFFFFF")
        self.karb_lista.heading(
            "id",
            text="Azonosító",
            command=lambda: self.evk_karbantartasi_lista_rendezese("id")
        )
        self.karb_lista.heading(
            "datum",
            text="Dátum",
            command=lambda: self.evk_karbantartasi_lista_rendezese("datum")
        )
        self.karb_lista.heading(
            "eszkoz",
            text="Eszköz",
            command=lambda: self.evk_karbantartasi_lista_rendezese("eszkoz")
        )
        self.karb_lista.heading(
            "leiras",
            text="Karbantartás leírása",
            command=lambda: self.evk_karbantartasi_lista_rendezese("leiras")
        )
        self.karb_lista.bind(
            "<<TreeviewSelect>>",
            self.evk_kijelolt_karbantartas_betoltese
        )
        karb_scrollbar = ttk.Scrollbar(
            karb_lista_frame,
            orient="vertical",
            command=self.karb_lista.yview
        )
        self.karb_lista.configure(yscrollcommand=karb_scrollbar.set)
        self.karb_lista.pack(side="left", fill="both", expand=True)
        karb_scrollbar.pack(side="right", fill="y")

        naplo_muveletek = ttk.Frame(naplo_frame)
        naplo_muveletek.pack(fill="x", pady=(4, 0))
        ttk.Button(
            naplo_muveletek,
            text="Kijelölt bejegyzés törlése",
            command=self.evk_karbantartas_torlese
        ).pack(side="left", padx=(0, 8), pady=4)
        ttk.Button(
            naplo_muveletek,
            text="Kijelölt bejegyzés módosítása",
            command=self.evk_karbantartas_modositasa
        ).pack(side="left", padx=8, pady=4)
        ttk.Button(
            naplo_muveletek,
            text="Napló mentése CSV-fájlba",
            command=self.evk_karbantartas_exportalasa
        ).pack(side="left", padx=8, pady=4)

    def evk_datum_atalakitasa(self, datum):
        for formatum in ("%Y.%m.%d.", "%Y.%m.%d"):
            try:
                return datetime.strptime(
                    datum,
                    formatum
                ).date().isoformat()
            except ValueError:
                pass
        return None

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

    def evk_eszkoz_db_frissitese(self):
        darab = self.kapcsolat.execute(
            "SELECT COUNT(*) FROM eszkozok"
        ).fetchone()[0]
        self.ossz_eszkoz_cimke.config(
            text=f"Nyilvántartott eszközök száma: {darab}"
        )

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

        for index, eszkoz in enumerate(eszkozok):
            cimke = "paros" if index % 2 == 0 else "paratlan"
            self.lista.insert(
                "",
                tk.END,
                values=eszkoz,
                tags=(cimke,)
            )

        self.evk_eszkoz_db_frissitese()
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

        datum = self.evk_datum_atalakitasa(
            self.datum_mezo.get().strip()
        )
        leiras = self.leiras_mezo.get().strip()

        if datum is None:
            messagebox.showwarning(
                "Hibás dátum",
                "A dátum formátuma legyen például "
                "2026.11.19. vagy 2026.11.19"
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
        datum_kereses = self.evk_datum_atalakitasa(kereses)

        if datum_kereses is not None:
            datum_minta = f"%{datum_kereses}%"
        else:
            datum_minta = minta

        bejegyzesek = self.kapcsolat.execute(
            "SELECT karbantartas.id, karbantartas.datum, "
            "eszkozok.nev, karbantartas.leiras "
            "FROM karbantartas "
            "JOIN eszkozok ON eszkozok.id = karbantartas.eszkoz_id "
            "WHERE karbantartas.datum LIKE ? "
            "OR eszkozok.nev LIKE ? "
            "OR karbantartas.leiras LIKE ? "
            "ORDER BY karbantartas.datum DESC",
            (datum_minta, minta, minta)
        ).fetchall()

        self.karb_db_cimke.config(
            text=(
                "Megjelenített naplóbejegyzések száma: "
                f"{len(bejegyzesek)}"
            )
        )

        for index, bejegyzes in enumerate(bejegyzesek):
            datum = datetime.strptime(
                bejegyzes[1],
                "%Y-%m-%d"
            ).strftime("%Y.%m.%d.")
            cimke = "paros" if index % 2 == 0 else "paratlan"
            self.karb_lista.insert(
                "",
                tk.END,
                values=(
                    bejegyzes[0],
                    datum,
                    bejegyzes[2],
                    bejegyzes[3]
                ),
                tags=(cimke,)
            )

        self.evk_kezdolap_statisztika_frissitese()

    def evk_kezdolap_statisztika_frissitese(self):
        eszkoz_db = self.kapcsolat.execute(
            "SELECT COUNT(*) FROM eszkozok"
        ).fetchone()[0]
        naplo_db = self.kapcsolat.execute(
            "SELECT COUNT(*) FROM karbantartas"
        ).fetchone()[0]
        utolso_datum = self.kapcsolat.execute(
            "SELECT MAX(datum) FROM karbantartas"
        ).fetchone()[0]

        self.kezdolap_eszkoz_szam.config(text=str(eszkoz_db))
        self.kezdolap_naplo_szam.config(text=str(naplo_db))

        if utolso_datum:
            megjelenitett_datum = datetime.strptime(
                utolso_datum,
                "%Y-%m-%d"
            ).strftime("%Y.%m.%d.")
        else:
            megjelenitett_datum = "Nincs adat"

        self.kezdolap_utolso_datum.config(text=megjelenitett_datum)

    def evk_eszkoz_lista_rendezese(self, oszlop, forditott=False):
        sorok = [
            (self.lista.set(sor, oszlop), sor)
            for sor in self.lista.get_children("")
        ]

        if oszlop == "id":
            sorok.sort(
                key=lambda adat: int(adat[0]),
                reverse=forditott
            )
        else:
            sorok.sort(
                key=lambda adat: adat[0].casefold(),
                reverse=forditott
            )

        for index, (_, sor) in enumerate(sorok):
            self.lista.move(sor, "", index)

        self.lista.heading(
            oszlop,
            command=lambda: self.evk_eszkoz_lista_rendezese(
                oszlop,
                not forditott
            )
        )

    def evk_karbantartasi_lista_rendezese(self, oszlop, forditott=False):
        sorok = [
            (self.karb_lista.set(sor, oszlop), sor)
            for sor in self.karb_lista.get_children("")
        ]

        if oszlop == "id":
            sorok.sort(
                key=lambda adat: int(adat[0]),
                reverse=forditott
            )
        else:
            sorok.sort(
                key=lambda adat: adat[0].casefold(),
                reverse=forditott
            )

        for index, (_, sor) in enumerate(sorok):
            self.karb_lista.move(sor, "", index)

        self.karb_lista.heading(
            oszlop,
            command=lambda: self.evk_karbantartasi_lista_rendezese(
                oszlop,
                not forditott
            )
        )

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

        datum = self.evk_datum_atalakitasa(
            self.datum_mezo.get().strip()
        )
        leiras = self.leiras_mezo.get().strip()

        if datum is None:
            messagebox.showwarning(
                "Hibás dátum",
                "A dátum formátuma legyen például "
                "2026.11.19. vagy 2026.11.19"
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

        export_mappa = Path(__file__).resolve().parent / "mintakimenetek"
        export_mappa.mkdir(exist_ok=True)
        fajlnev = filedialog.asksaveasfilename(
            title="Karbantartási napló mentése",
            initialdir=str(export_mappa),
            initialfile="karbantartasi_naplo.csv",
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

                for datum, eszkoz, leiras in bejegyzesek:
                    datum = datetime.strptime(
                        datum,
                        "%Y-%m-%d"
                    ).strftime("%Y.%m.%d.")
                    iro.writerow((datum, eszkoz, leiras))
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

        export_mappa = Path(__file__).resolve().parent / "mintakimenetek"
        export_mappa.mkdir(exist_ok=True)
        fajlnev = filedialog.asksaveasfilename(
            title="Eszközlista mentése",
            initialdir=str(export_mappa),
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

    def evk_ablak_bezarasa(self):
        self.kapcsolat.close()
        self.root.destroy()
