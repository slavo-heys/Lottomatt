from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from time import strftime
import random
from PIL import ImageTk, Image

# Tworzenie bazy , jeśli nie istnieje
conn = sqlite3.connect('baza.db')
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS lotto(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dzien int NOT NULL,
        miesiac int NOT NULL,
        rok int NOT NULL,
        nr_losowania int NOT NULL,
        l1 int NOT NULL,
        l2 int NOT NULL,
        l3 int NOT NULL,
        l4 int NOT NULL,
        l5 int NOT NULL,
        l6 int NOT NULL);"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS liczbyUser(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dzien int NOT NULL,
        miesiac int NOT NULL,
        rok int NOT NULL,
        lu1 int NOT NULL,
        lu2 int NOT NULL,
        lu3 int NOT NULL,
        lu4 int NOT NULL,
        lu5 int NOT NULL,
        lu6 int NOT NULL
    );"""
)
conn.commit()
conn.close()


class Program:
    def __init__(self, master):

        def MenuRozwijane(self):
            menu = Menu(root)

            new_item = Menu(menu)
            menu.add_cascade(label="Program", menu=new_item)
            new_item.add_command(label="rejestracja użytkownika", command="")
            new_item.add_separator()
            new_item.add_command(label="wyjście z programu", command="")

            new_obsl = Menu(menu)
            menu.add_cascade(label="Help", menu=new_obsl)
            new_obsl.add_command(label="pomoc", command="")

            root.config(menu=menu)

        MenuRozwijane(self)

        self.ramka = Frame(root, height=596, width=160, bg="#FAEBD7")
        self.ramka.pack(padx=5, pady=5, side=LEFT)

        linia = tk.Label(self.ramka, text="moja ramka", justify=LEFT)
        linia.place(x=500, y=10)

        but0 = tk.Button(self.ramka, text="Dodaj losowanie",
                         width=18, command=self.dodaj_losowanie)
        but0.place(x=10, y=10)

        but1 = tk.Button(self.ramka, text="Dodaj swoje liczby ",
                         width=18, command=self.dodaj_liczby)
        but1.place(x=10, y=40)

        but2 = tk.Button(
            self.ramka, text="Powtarzające się liczby", width=18, command="")
        but2.place(x=10, y=70)

        but3 = tk.Button(self.ramka, text="Analiza par", width=18, command="")
        but3.place(x=10, y=100)

        but4 = tk.Button(self.ramka, text="Sprawdź moje liczby",
                         width=18, command="")
        but4.place(x=10, y=130)

        but4 = tk.Button(self.ramka, text="Wyjście z programu",
                         bg="#F08080", width=18, command=self.zamknij_program)
        but4.place(x=10, y=540)

    def dodaj_losowanie(self):
        self.ramka1 = Frame(root,  height=596, width=650, bg="#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side=RIGHT)

        # Formularz - dodaj liczby z losowania
        l1 = tk.Label(self.ramka1, text="Wstaw datę losowania:",
                      font=("Arial", 13), bg="#FAFAD2")
        l1.place(x=10, y=10)

        l1a = tk.Label(self.ramka1, text="dd:",
                       font=("Arial", 13), bg="#FAFAD2")
        l1a.place(x=200, y=10)

        l1b = tk.Label(self.ramka1, text="mm:",
                       font=("Arial", 13), bg="#FAFAD2")
        l1b.place(x=280, y=10)

        l1c = tk.Label(self.ramka1, text="yyyy:",
                       font=("Arial", 13), bg="#FAFAD2")
        l1c.place(x=360, y=10)

        l2 = tk.Label(self.ramka1, text="Wstaw numer losowania:",
                      font=("Arial", 13), bg="#FAFAD2")
        l2.place(x=10, y=35)

        l3 = tk.Label(self.ramka1, text="Podaj sześć liczb:",
                      font=("Arial", 13), bg="#FAFAD2")
        l3.place(x=10, y=70)

        self.dzien = StringVar()
        e1 = tk.Entry(self.ramka1, textvariable=self.dzien,
                      font=("Arial", 13), width=3)
        e1.place(x=229, y=10)

        self.miesiac = StringVar()
        e1a = tk.Entry(self.ramka1, textvariable=self.miesiac,
                       font=("Arial", 13), width=3)
        e1a.place(x=316, y=10)

        self.rok = StringVar()
        e1a = tk.Entry(self.ramka1, textvariable=self.rok,
                       font=("Arial", 13), width=5)
        e1a.place(x=407, y=10)

        self.nLosowania = StringVar()
        e2 = tk.Entry(self.ramka1, textvariable=self.nLosowania,
                      font=("Arial", 13), width=8)
        e2.place(x=200, y=35)
        # liczba1
        self.licz1 = StringVar()
        e3 = tk.Entry(self.ramka1, textvariable=self.licz1,
                      font=("Arial", 13), width=2)
        e3.place(x=200, y=70)
        # liczba2
        self.licz2 = StringVar()
        e4 = tk.Entry(self.ramka1, textvariable=self.licz2,
                      font=("Arial", 13), width=2)
        e4.place(x=230, y=70)
        # liczba 3
        self.licz3 = StringVar()
        e5 = tk.Entry(self.ramka1, textvariable=self.licz3,
                      font=("Arial", 13), width=2)
        e5.place(x=260, y=70)
        # liczba 4
        self.licz4 = StringVar()
        e6 = tk.Entry(self.ramka1, textvariable=self.licz4,
                      font=("Arial", 13), width=2)
        e6.place(x=290, y=70)
        # liczba 5
        self.licz5 = StringVar()
        e7 = tk.Entry(self.ramka1, textvariable=self.licz5,
                      font=("Arial", 13), width=2)
        e7.place(x=320, y=70)
        # liczba 6
        self.licz6 = StringVar()
        e8 = tk.Entry(self.ramka1, textvariable=self.licz6,
                      font=("Arial", 13), width=2)
        e8.place(x=350, y=70)
        # przycisk zapisz do tabli i wyczyść dane
        przycisk1 = tk.Button(self.ramka1, text="Zapisz do bazy",
                              bg="#F08080", command=self.zapisz_do_bazy)
        przycisk1.place(x=310, y=100)

        przycisk2 = tk.Button(self.ramka1, text="Wyczyść dane",
                              bg="#90EE90", command=self.clear_dane)
        przycisk2.place(x=210, y=100)

    def zapisz_do_bazy(self):
        return

    def clear_dane(self):
        return

    def dodaj_liczby(self):
        self.ramka1 = Frame(root,  height=596, width=650, bg="#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side=RIGHT)

    def powtarzajace_liczby(self):
        self.ramka1 = Frame(root,  height=596, width=650, bg="#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side=RIGHT)

    def analiza_par(self):
        self.ramka1 = Frame(root,  height=596, width=650, bg="#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side=RIGHT)

    def sprawdz_wyniki(self):
        self.ramka1 = Frame(root,  height=596, width=650, bg="#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side=RIGHT)

    def zamknij_program(self):
        root.destroy()


root = tk.Tk()
root.geometry("800x600+100+100")  # rozmiar i położenie okna
root.title("Lottomat")  # tytuł okna
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='lotto.png'))
root.resizable(False, False)  # blokowanie rozmiaru okienka

Program(root)  # uruchomienie programu

root.mainloop()
