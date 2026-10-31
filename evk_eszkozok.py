import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class EVKEszkozNyilvantarto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eszköznyilvántartó")
        self.geometry("600x400")
        self.kapcsolat = sqlite3.connect("eszkozok.db")
        self.evk_adatbazis_elokeszitese()
        self.evk_felulet_elkeszitese()
        self.evk_lista_frissitese()

    def evk_adatbazis_elokeszitese(self):
        self.kapcsolat.execute(
            "CREATE TABLE IF NOT EXISTS eszkozok "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "nev TEXT NOT NULL, kategoria TEXT NOT NULL)"
        )
        self.kapcsolat.commit()

    def evk_felulet_elkeszitese(self):
        beviteli_sor = ttk.Frame(self, padding=10)
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

        self.lista = ttk.Treeview(
            self,
            columns=("id", "nev", "kategoria"),
            show="headings"
        )
        self.lista.heading("id", text="Azonosító")
        self.lista.heading("nev", text="Eszköz neve")
        self.lista.heading("kategoria", text="Kategória")
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(
            self,
            text="Kijelölt eszköz törlése",
            command=self.evk_eszkoz_torlese
        ).pack(pady=(0, 10))

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

    def evk_lista_frissitese(self):
        for sor in self.lista.get_children():
            self.lista.delete(sor)

        eszkozok = self.kapcsolat.execute(
            "SELECT id, nev, kategoria FROM eszkozok ORDER BY nev"
        ).fetchall()

        for eszkoz in eszkozok:
            self.lista.insert("", tk.END, values=eszkoz)

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
            f"Biztosan törlöd ezt az eszközt: {eszkoz[1]}?"
        )

        if biztos:
            self.kapcsolat.execute(
                "DELETE FROM eszkozok WHERE id = ?",
                (eszkoz[0],)
            )
            self.kapcsolat.commit()
            self.evk_lista_frissitese()