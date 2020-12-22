from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from time import strftime
import random
from PIL import ImageTk, Image
import time
from tkinter.messagebox import showinfo
from operator import itemgetter
import requests
import json
import csv

# Tworzenie bazy , jeśli nie istnieje
conn = sqlite3.connect('baza.db')
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS lotto(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nr_losowania text NOT NULL,
        data text NOT NULL,
        l1 text NOT NULL,
        l2 text NOT NULL,
        l3 text NOT NULL,
        l4 text NOT NULL,
        l5 text NOT NULL,
        l6 text NOT NULL);"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS liczbyUser(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dzien text NOT NULL,
        miesiac text NOT NULL,
        rok text NOT NULL,
        lu1 text NOT NULL,
        lu2 text NOT NULL,
        lu3 text NOT NULL,
        lu4 text NOT NULL,
        lu5 text NOT NULL,
        lu6 text NOT NULL
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
            #new_item.add_command(label="rejestracja użytkownika", command=self.rejestracja_usera)
            # new_item.add_separator()
            new_item.add_command(label="wyjście z programu",
                                 command=self.zamknij_program)

            #new_obsl = Menu(menu)
            #menu.add_cascade(label="Inne", menu=new_obsl)
            #new_obsl.add_command(label="pomoc", command="")
            # new_item.add_separator()

            root.config(menu=menu)

        MenuRozwijane(self)

        self.ramka = Frame(root, height=596, width=160, bg="#FAEBD7")
        self.ramka.pack(padx=5, pady=5, side=LEFT)

        but0 = tk.Button(self.ramka, text="Ostatnie losowanie",
                         width=18, command=self.wyniki_losowania)
        but0.place(x=10, y=10)

        but7 = tk.Button(self.ramka, text="Import z pliku csv",
                         width=18, command=self.update)
        but7.place(x=10, y=40)

        but1 = tk.Button(self.ramka, text="Dodaj swoje liczby ",
                         width=18, command=self.dodaj_liczby)
        but1.place(x=10, y=70)

        but2 = tk.Button(self.ramka, text="Analiza liczb",
                         width=18, command=self.liczby_powtorzone)
        but2.place(x=10, y=160)

        but3 = tk.Button(self.ramka, text="Analiza par",
                         width=18, command=self.analiza_par)
        but3.place(x=10, y=160)

        but5 = tk.Button(self.ramka, text="Analiza trójek",
                         width=18, command=self.analiza_trojek)
        but5.place(x=10, y=190)

        but6 = tk.Button(self.ramka, text="Analiza czwórek",
                         width=18, command=self.analiza_czworek)
        but6.place(x=10, y=220)

        but4 = tk.Button(self.ramka, text="Sprawdź moje liczby",
                         width=18, command=self.weryfikacja_liczb)
        but4.place(x=10, y=100)

        but4 = tk.Button(self.ramka, text="Wyjście z programu",
                         bg="#F08080", width=18, command=self.zamknij_program)
        but4.place(x=10, y=540)

# definicja aktualizacji z pliku csv
    def update(self):
        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("Delete from lotto")

        with open('lotto.csv', 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')

            for row in csvreader:
                losowanie = (row[0])
                dataLos = (row[1])
                licz1 = (row[2])
                licz2 = (row[3])
                licz3 = (row[4])
                licz4 = (row[5])
                licz5 = (row[6])
                licz6 = (row[7])

                c.execute("INSERT INTO lotto VALUES(NULL, :nr_losowania, :data, :l1, :l2, :l3, :l4, :l5, :l6)",
                          {
                              'nr_losowania': losowanie,
                              'data': dataLos,
                              'l1': licz1,
                              'l2': licz2,
                              'l3': licz3,
                              'l4': licz4,
                              'l5': licz5,
                              'l6': licz6
                          })
        conn.commit()
        conn.close()
        self.baza_csv()

# definicja sprawdzania wyników losowania
    def wyniki_losowania(self):
        r = requests.get(
            'http://serwis.mobilotto.pl/mapi_v6/index.php?json=getGames')

        html_text: str = r.text
        json_text: dict = r.json()
        r.encoding = 'utf-8'

        text = (r.text)
        wynik = json.loads(text)

        b = (wynik['Lotto'])
        numerki = (b['numerki'])
        liczby_p = numerki.split(',')
        liczby = []
        liczby.append(int(liczby_p[0]))
        liczby.append(int(liczby_p[1]))
        liczby.append(int(liczby_p[2]))
        liczby.append(int(liczby_p[3]))
        liczby.append(int(liczby_p[4]))
        liczby.append(int(liczby_p[5]))
        

        liczby.sort()

        nrLosowania = (b['num_losowania'])
        data = (b['data_losowania'])
        data = data[0:10]

        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lotto")
        records = c.fetchall()
        for rec in records:
            numerLosowania = str(rec[1])
            dataOstatnia = str(rec[2])
        conn.close()

        if numerLosowania == nrLosowania or dataOstatnia == data:
            self.ramka1 = Frame(root,  height=300, width=650, bg="green")
            self.ramka1.pack(padx=5, pady=5, side=TOP)
            tk.Label(self.ramka1, text="Losowanie już istnieje w bazie!", font=(
                "Arial, 14"), bg="green", fg="white").place(x=20, y=20)
            tk.Label(self.ramka1, text="Ostatnie wyniki Dużego Lotka: "+str(liczby[0])+" , "+str(liczby[1])+" , "+str(liczby[2])+" , "+str(
                liczby[3])+" , "+str(liczby[4])+" , "+str(liczby[5]), font=("Arial", 14), fg="white", bg="green").place(x=80, y=150)
            but = tk.Button(self.ramka1, text="zamknij to okno",
                            bg="#DC143C", command=self.zamknij_okno)
            but.place(x=260, y=250)
        else:
            conn = sqlite3.connect('baza.db')
            c = conn.cursor()
            c.execute("INSERT INTO lotto VALUES(NULL, :nr_losowania, :data, :l1, :l2, :l3, :l4, :l5, :l6)",
                      {
                          'nr_losowania': nrLosowania,
                          'data': data,
                          'l1': liczby[0],
                          'l2': liczby[1],
                          'l3': liczby[2],
                          'l4': liczby[3],
                          'l5': liczby[4],
                          'l6': liczby[5]
                      })
            conn.commit()
            conn.close()
            self.ramka1 = Frame(root,  height=300, width=650, bg="green")
            self.ramka1.pack(padx=5, pady=5, side=TOP)
            tk.Label(self.ramka1, text="Losowanie  zapisane!", font=(
                "Arial, 14"), bg="green", fg="white").place(x=20, y=20)
            tk.Label(self.ramka1, text="Ostatnie wyniki Dużego Lotka: "+str(liczby[0])+" , "+str(liczby[1])+" , "+str(liczby[2])+" , "+str(
                liczby[3])+" , "+str(liczby[4])+" , "+str(liczby[5]), font=("Arial", 14), fg="white", bg="green").place(x=80, y=150)
            but = tk.Button(self.ramka1, text="zamknij to okno",
                            bg="#DC143C", command=self.zamknij_okno)
            but.place(x=260, y=250)


# definicja analizy czworek

    def analiza_czworek(self):
        self.ramka1 = Frame(root,  height=596, width=650, bg="#ADD8E6")
        self.ramka1.pack(padx=5, pady=5, side=RIGHT)
        czworki = []

        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lotto")
        records = c.fetchall()
        for rec in records:
            l1 = str(rec[3])
            l1 = int(l1)

            l2 = str(rec[4])
            l2 = int(l2)

            l3 = str(rec[5])
            l3 = int(l3)

            l4 = str(rec[6])
            l4 = int(l4)

            l5 = str(rec[7])
            l5 = int(l5)

            l6 = str(rec[8])
            l6 = int(l6)

        for w in range(1, 50):
            for e in range(1, 50):
                for r in range(1, 50):
                    for t in range(1, 50):
                        if l1 == w and l2 == e and l3 == r and l4 == t:
                            czworki.append([l1, l2, l3, l4])
                        elif l1 == w and l2 == e and l3 == r and l5 == t:
                            czworki.append([l1, l2, l3, l5])
                        elif l1 == w and l2 == e and l3 == r and l6 == t:
                            czworki.append([l1, l2, l3, l6])
                        elif l1 == w and l2 == e and l4 == r and l3 == t:
                            czworki.append([l1, l2, l4, l3])
                        elif l1 == w and l2 == e and l4 == r and l5 == t:
                            czworki.append([l1, l2, l4, l5])
                        elif l1 == w and l2 == e and l4 == r and l6 == t:
                            czworki.append([l1, l2, l4, l6])
                        elif l1 == w and l2 == e and l5 == r and l3 == t:
                            czworki.append([l1, l2, l5, l3])
                        elif l1 == w and l2 == e and l5 == r and l4 == t:
                            czworki.append([l1, l2, l5, l4])
                        elif l1 == w and l2 == e and l5 == r and l6 == t:
                            czworki.append([l1, l2, l5, l6])
                        elif l1 == w and l2 == e and l6 == r and l3 == t:
                            czworki.append([l1, l2, l6, l3])
                        elif l1 == w and l2 == e and l6 == r and l4 == t:
                            czworki.append([l1, l2, l6, l4])
                        elif l1 == w and l2 == e and l6 == r and l5 == t:
                            czworki.append([l1, l2, l6, l5])
                        elif l1 == w and l3 == e and l2 == r and l4 == t:
                            czworki.append([l1, l3, l2, l4])
                        elif l1 == w and l3 == e and l2 == r and l5 == t:
                            czworki.append([l1, l3, l2, l5])
                        elif l1 == w and l3 == e and l2 == r and l6 == t:
                            czworki.append([l1, l3, l2, l6])
                        elif l1 == w and l3 == e and l4 == r and l2 == t:
                            czworki.append([l1, l3, l4, l2])
                        elif l1 == w and l3 == e and l4 == r and l5 == t:
                            czworki.append([l1, l3, l4, l5])
                        elif l1 == w and l3 == e and l4 == r and l6 == t:
                            czworki.append([l1, l3, l4, l6])
                        elif l1 == w and l3 == e and l5 == r and l2 == t:
                            czworki.append([l1, l3, l5, l2])
                        elif l1 == w and l3 == e and l5 == r and l4 == t:
                            czworki.append([l1, l3, l5, l4])
                        elif l1 == w and l3 == e and l5 == r and l6 == t:
                            czworki.append([l1, l3, l5, l6])
                        elif l1 == w and l3 == e and l6 == r and l2 == t:
                            czworki.append([l1, l3, l6, l2])
                        elif l1 == w and l3 == e and l6 == r and l4 == t:
                            czworki.append([l1, l3, l6, l4])
                        elif l1 == w and l3 == e and l6 == r and l5 == t:
                            czworki.append([l1, l3, l6, l5])
                        elif l1 == w and l4 == e and l2 == r and l3 == t:
                            czworki.append([l1, l4, l2, l3])
                        elif l1 == w and l4 == e and l2 == r and l5 == t:
                            czworki.append([l1, l4, l2, l5])
                        elif l1 == w and l4 == e and l2 == r and l6 == t:
                            czworki.append([l1, l4, l2, l6])
                        elif l1 == w and l4 == e and l3 == r and l2 == t:
                            czworki.append([l1, l4, l3, l2])
                        elif l1 == w and l4 == e and l3 == r and l5 == t:
                            czworki.append([l1, l4, l3, l5])
                        elif l1 == w and l4 == e and l3 == r and l6 == t:
                            czworki.append([l1, l4, l3, l6])
                        elif l1 == w and l4 == e and l5 == r and l2 == t:
                            czworki.append([l1, l4, l5, l2])
                        elif l1 == w and l4 == e and l5 == r and l3 == t:
                            czworki.append([l1, l4, l5, l3])
                        elif l1 == w and l4 == e and l5 == r and l6 == t:
                            czworki.append([l1, l4, l5, l6])
                        elif l1 == w and l4 == e and l6 == r and l2 == t:
                            czworki.append([l1, l4, l6, l2])
                        elif l1 == w and l4 == e and l6 == r and l3 == t:
                            czworki.append([l1, l4, l6, l3])
                        elif l1 == w and l4 == e and l6 == r and l5 == t:
                            czworki.append([l1, l4, l6, l5])
                        elif l1 == w and l5 == e and l2 == r and l3 == t:
                            czworki.append([l1, l5, l2, l3])
                        elif l1 == w and l5 == e and l2 == r and l4 == t:
                            czworki.append([l1, l5, l2, l4])
                        elif l1 == w and l5 == e and l2 == r and l6 == t:
                            czworki.append([l1, l5, l2, l6])
                        elif l1 == w and l5 == e and l3 == r and l2 == t:
                            czworki.append([l1, l5, l3, l2])
                        elif l1 == w and l5 == e and l3 == r and l4 == t:
                            czworki.append([l1, l5, l3, l4])
                        elif l1 == w and l5 == e and l3 == r and l6 == t:
                            czworki.append([l1, l5, l3, l6])
                        elif l1 == w and l5 == e and l4 == r and l2 == t:
                            czworki.append([l1, l5, l4, l2])
                        elif l1 == w and l5 == e and l4 == r and l3 == t:
                            czworki.append([l1, l5, l4, l3])
                        elif l1 == w and l5 == e and l4 == r and l6 == t:
                            czworki.append([l1, l5, l4, l6])
                        elif l1 == w and l5 == e and l6 == r and l2 == t:
                            czworki.append([l1, l5, l6, l2])
                        elif l1 == w and l5 == e and l6 == r and l3 == t:
                            czworki.append([l1, l5, l6, l3])
                        elif l1 == w and l5 == e and l6 == r and l4 == t:
                            czworki.append([l1, l5, l6, l4])
                        elif l1 == w and l6 == e and l2 == r and l3 == t:
                            czworki.append([l1, l6, l2, l3])
                        elif l1 == w and l6 == e and l2 == r and l4 == t:
                            czworki.append([l1, l6, l2, l4])
                        elif l1 == w and l6 == e and l2 == r and l5 == t:
                            czworki.append([l1, l6, l2, l5])
                        elif l1 == w and l6 == e and l3 == r and l2 == t:
                            czworki.append([l1, l6, l3, l2])
                        elif l1 == w and l6 == e and l3 == r and l4 == t:
                            czworki.append([l1, l6, l3, l4])
                        elif l1 == w and l6 == e and l3 == r and l5 == t:
                            czworki.append([l1, l6, l3, l5])
                        elif l1 == w and l6 == e and l4 == r and l2 == t:
                            czworki.append([l1, l6, l4, l2])
                        elif l1 == w and l6 == e and l4 == r and l3 == t:
                            czworki.append([l1, l6, l4, l3])
                        elif l1 == w and l6 == e and l4 == r and l5 == t:
                            czworki.append([l1, l6, l4, l5])
                        elif l1 == w and l6 == e and l5 == r and l2 == t:
                            czworki.append([l1, l6, l5, l2])
                        elif l1 == w and l6 == e and l5 == r and l3 == t:
                            czworki.append([l1, l6, l5, l3])
                        elif l1 == w and l6 == e and l5 == r and l4 == t:
                            czworki.append([l1, l6, l5, l4])
                        elif l2 == w and l1 == e and l3 == r and l4 == t:
                            czworki.append([l2, l1, l3, l4])
                        elif l2 == w and l1 == e and l3 == r and l5 == t:
                            czworki.append([l2, l1, l3, l5])
                        elif l2 == w and l1 == e and l3 == r and l6 == t:
                            czworki.append([l2, l1, l3, l6])
                        elif l2 == w and l1 == e and l4 == r and l3 == t:
                            czworki.append([l2, l1, l4, l3])
                        elif l2 == w and l1 == e and l4 == r and l5 == t:
                            czworki.append([l2, l1, l4, l5])
                        elif l2 == w and l1 == e and l4 == r and l6 == t:
                            czworki.append([l2, l1, l4, l6])
                        elif l2 == w and l1 == e and l5 == r and l3 == t:
                            czworki.append([l2, l1, l5, l3])
                        elif l2 == w and l1 == e and l5 == r and l4 == t:
                            czworki.append([l2, l1, l5, l4])
                        elif l2 == w and l1 == e and l5 == r and l6 == t:
                            czworki.append([l2, l1, l5, l6])
                        elif l2 == w and l1 == e and l6 == r and l3 == t:
                            czworki.append([l2, l1, l6, l3])
                        elif l2 == w and l1 == e and l6 == r and l4 == t:
                            czworki.append([l2, l1, l6, l4])
                        elif l2 == w and l1 == e and l6 == r and l5 == t:
                            czworki.append([l2, l1, l6, l5])
                        elif l2 == w and l3 == e and l1 == r and l4 == t:
                            czworki.append([l2, l3, l1, l4])
                        elif l2 == w and l3 == e and l1 == r and l5 == t:
                            czworki.append([l2, l3, l1, l5])
                        elif l2 == w and l3 == e and l1 == r and l6 == t:
                            czworki.append([l2, l3, l1, l6])
                        elif l2 == w and l3 == e and l4 == r and l1 == t:
                            czworki.append([l2, l3, l4, l1])
                        elif l2 == w and l3 == e and l4 == r and l5 == t:
                            czworki.append([l2, l3, l4, l5])
                        elif l2 == w and l3 == e and l4 == r and l6 == t:
                            czworki.append([l2, l3, l4, l6])
                        elif l2 == w and l3 == e and l5 == r and l1 == t:
                            czworki.append([l2, l3, l5, l1])
                        elif l2 == w and l3 == e and l5 == r and l4 == t:
                            czworki.append([l2, l3, l5, l4])
                        elif l2 == w and l3 == e and l5 == r and l6 == t:
                            czworki.append([l2, l3, l5, l6])
                        elif l2 == w and l3 == e and l6 == r and l1 == t:
                            czworki.append([l2, l3, l6, l1])
                        elif l2 == w and l3 == e and l6 == r and l4 == t:
                            czworki.append([l2, l3, l6, l4])
                        elif l2 == w and l3 == e and l6 == r and l5 == t:
                            czworki.append([l2, l3, l6, l5])
                        elif l2 == w and l4 == e and l1 == r and l3 == t:
                            czworki.append([l2, l4, l1, l3])
                        elif l2 == w and l4 == e and l1 == r and l5 == t:
                            czworki.append([l2, l4, l1, l5])
                        elif l2 == w and l4 == e and l1 == r and l6 == t:
                            czworki.append([l2, l4, l1, l6])
                        elif l2 == w and l4 == e and l3 == r and l1 == t:
                            czworki.append([l2, l4, l3, l1])
                        elif l2 == w and l4 == e and l3 == r and l5 == t:
                            czworki.append([l2, l4, l3, l5])
                        elif l2 == w and l4 == e and l3 == r and l6 == t:
                            czworki.append([l2, l4, l3, l6])
                        elif l2 == w and l4 == e and l5 == r and l1 == t:
                            czworki.append([l2, l4, l5, l1])
                        elif l2 == w and l4 == e and l5 == r and l3 == t:
                            czworki.append([l2, l4, l5, l3])
                        elif l2 == w and l4 == e and l5 == r and l6 == t:
                            czworki.append([l2, l4, l5, l6])
                        elif l2 == w and l4 == e and l6 == r and l1 == t:
                            czworki.append([l2, l4, l6, l1])
                        elif l2 == w and l4 == e and l6 == r and l3 == t:
                            czworki.append([l2, l4, l6, l3])
                        elif l2 == w and l4 == e and l6 == r and l5 == t:
                            czworki.append([l2, l4, l6, l5])
                        elif l2 == w and l5 == e and l1 == r and l3 == t:
                            czworki.append([l2, l5, l1, l3])
                        elif l2 == w and l5 == e and l1 == r and l4 == t:
                            czworki.append([l2, l5, l1, l4])
                        elif l2 == w and l5 == e and l1 == r and l6 == t:
                            czworki.append([l2, l5, l1, l6])
                        elif l2 == w and l5 == e and l3 == r and l1 == t:
                            czworki.append([l2, l5, l3, l1])
                        elif l2 == w and l5 == e and l3 == r and l4 == t:
                            czworki.append([l2, l5, l3, l4])
                        elif l2 == w and l5 == e and l3 == r and l6 == t:
                            czworki.append([l2, l5, l3, l6])
                        elif l2 == w and l5 == e and l4 == r and l1 == t:
                            czworki.append([l2, l5, l4, l1])
                        elif l2 == w and l5 == e and l4 == r and l3 == t:
                            czworki.append([l2, l5, l4, l3])
                        elif l2 == w and l5 == e and l4 == r and l6 == t:
                            czworki.append([l2, l5, l4, l6])
                        elif l2 == w and l5 == e and l6 == r and l1 == t:
                            czworki.append([l2, l5, l6, l1])
                        elif l2 == w and l5 == e and l6 == r and l3 == t:
                            czworki.append([l2, l5, l6, l3])
                        elif l2 == w and l5 == e and l6 == r and l4 == t:
                            czworki.append([l2, l5, l6, l4])
                        elif l2 == w and l6 == e and l1 == r and l3 == t:
                            czworki.append([l2, l6, l1, l3])
                        elif l2 == w and l6 == e and l1 == r and l4 == t:
                            czworki.append([l2, l6, l1, l4])
                        elif l2 == w and l6 == e and l1 == r and l5 == t:
                            czworki.append([l2, l6, l1, l5])
                        elif l2 == w and l6 == e and l3 == r and l1 == t:
                            czworki.append([l2, l6, l3, l1])
                        elif l2 == w and l6 == e and l3 == r and l4 == t:
                            czworki.append([l2, l6, l3, l4])
                        elif l2 == w and l6 == e and l3 == r and l5 == t:
                            czworki.append([l2, l6, l3, l5])
                        elif l2 == w and l6 == e and l4 == r and l1 == t:
                            czworki.append([l2, l6, l4, l1])
                        elif l2 == w and l6 == e and l4 == r and l3 == t:
                            czworki.append([l2, l6, l4, l3])
                        elif l2 == w and l6 == e and l4 == r and l5 == t:
                            czworki.append([l2, l6, l4, l5])
                        elif l2 == w and l6 == e and l5 == r and l1 == t:
                            czworki.append([l2, l6, l5, l1])
                        elif l2 == w and l6 == e and l5 == r and l3 == t:
                            czworki.append([l2, l6, l5, l3])
                        elif l2 == w and l6 == e and l5 == r and l4 == t:
                            czworki.append([l2, l6, l5, l4])
                        elif l3 == w and l1 == e and l2 == r and l4 == t:
                            czworki.append([l3, l1, l2, l4])
                        elif l3 == w and l1 == e and l2 == r and l5 == t:
                            czworki.append([l3, l1, l2, l5])
                        elif l3 == w and l1 == e and l2 == r and l6 == t:
                            czworki.append([l3, l1, l2, l6])
                        elif l3 == w and l1 == e and l4 == r and l2 == t:
                            czworki.append([l3, l1, l4, l2])
                        elif l3 == w and l1 == e and l4 == r and l5 == t:
                            czworki.append([l3, l1, l4, l5])
                        elif l3 == w and l1 == e and l4 == r and l6 == t:
                            czworki.append([l3, l1, l4, l6])
                        elif l3 == w and l1 == e and l5 == r and l2 == t:
                            czworki.append([l3, l1, l5, l2])
                        elif l3 == w and l1 == e and l5 == r and l4 == t:
                            czworki.append([l3, l1, l5, l4])
                        elif l3 == w and l1 == e and l5 == r and l6 == t:
                            czworki.append([l3, l1, l5, l6])
                        elif l3 == w and l1 == e and l6 == r and l2 == t:
                            czworki.append([l3, l1, l6, l2])
                        elif l3 == w and l1 == e and l6 == r and l4 == t:
                            czworki.append([l3, l1, l6, l4])
                        elif l3 == w and l1 == e and l6 == r and l5 == t:
                            czworki.append([l3, l1, l6, l5])
                        elif l3 == w and l2 == e and l1 == r and l4 == t:
                            czworki.append([l3, l2, l1, l4])
                        elif l3 == w and l2 == e and l1 == r and l5 == t:
                            czworki.append([l3, l2, l1, l5])
                        elif l3 == w and l2 == e and l1 == r and l6 == t:
                            czworki.append([l3, l2, l1, l6])
                        elif l3 == w and l2 == e and l4 == r and l1 == t:
                            czworki.append([l3, l2, l4, l1])
                        elif l3 == w and l2 == e and l4 == r and l5 == t:
                            czworki.append([l3, l2, l4, l5])
                        elif l3 == w and l2 == e and l4 == r and l6 == t:
                            czworki.append([l3, l2, l4, l6])
                        elif l3 == w and l2 == e and l5 == r and l1 == t:
                            czworki.append([l3, l2, l5, l1])
                        elif l3 == w and l2 == e and l5 == r and l4 == t:
                            czworki.append([l3, l2, l5, l4])
                        elif l3 == w and l2 == e and l5 == r and l6 == t:
                            czworki.append([l3, l2, l5, l6])
                        elif l3 == w and l2 == e and l6 == r and l1 == t:
                            czworki.append([l3, l2, l6, l1])
                        elif l3 == w and l2 == e and l6 == r and l4 == t:
                            czworki.append([l3, l2, l6, l4])
                        elif l3 == w and l2 == e and l6 == r and l5 == t:
                            czworki.append([l3, l2, l6, l5])
                        elif l3 == w and l4 == e and l1 == r and l2 == t:
                            czworki.append([l3, l4, l1, l2])
                        elif l3 == w and l4 == e and l1 == r and l5 == t:
                            czworki.append([l3, l4, l1, l5])
                        elif l3 == w and l4 == e and l1 == r and l6 == t:
                            czworki.append([l3, l4, l1, l6])
                        elif l3 == w and l4 == e and l2 == r and l1 == t:
                            czworki.append([l3, l4, l2, l1])
                        elif l3 == w and l4 == e and l2 == r and l5 == t:
                            czworki.append([l3, l4, l2, l5])
                        elif l3 == w and l4 == e and l2 == r and l6 == t:
                            czworki.append([l3, l4, l2, l6])
                        elif l3 == w and l4 == e and l5 == r and l1 == t:
                            czworki.append([l3, l4, l5, l1])
                        elif l3 == w and l4 == e and l5 == r and l2 == t:
                            czworki.append([l3, l4, l5, l2])
                        elif l3 == w and l4 == e and l5 == r and l6 == t:
                            czworki.append([l3, l4, l5, l6])
                        elif l3 == w and l4 == e and l6 == r and l1 == t:
                            czworki.append([l3, l4, l6, l1])
                        elif l3 == w and l4 == e and l6 == r and l2 == t:
                            czworki.append([l3, l4, l6, l2])
                        elif l3 == w and l4 == e and l6 == r and l5 == t:
                            czworki.append([l3, l4, l6, l5])
                        elif l3 == w and l5 == e and l1 == r and l2 == t:
                            czworki.append([l3, l5, l1, l2])
                        elif l3 == w and l5 == e and l1 == r and l4 == t:
                            czworki.append([l3, l5, l1, l4])
                        elif l3 == w and l5 == e and l1 == r and l6 == t:
                            czworki.append([l3, l5, l1, l6])
                        elif l3 == w and l5 == e and l2 == r and l1 == t:
                            czworki.append([l3, l5, l2, l1])
                        elif l3 == w and l5 == e and l2 == r and l4 == t:
                            czworki.append([l3, l5, l2, l4])
                        elif l3 == w and l5 == e and l2 == r and l6 == t:
                            czworki.append([l3, l5, l2, l6])
                        elif l3 == w and l5 == e and l4 == r and l1 == t:
                            czworki.append([l3, l5, l4, l1])
                        elif l3 == w and l5 == e and l4 == r and l2 == t:
                            czworki.append([l3, l5, l4, l2])
                        elif l3 == w and l5 == e and l4 == r and l6 == t:
                            czworki.append([l3, l5, l4, l6])
                        elif l3 == w and l5 == e and l6 == r and l1 == t:
                            czworki.append([l3, l5, l6, l1])
                        elif l3 == w and l5 == e and l6 == r and l2 == t:
                            czworki.append([l3, l5, l6, l2])
                        elif l3 == w and l5 == e and l6 == r and l4 == t:
                            czworki.append([l3, l5, l6, l4])
                        elif l3 == w and l6 == e and l1 == r and l2 == t:
                            czworki.append([l3, l6, l1, l2])
                        elif l3 == w and l6 == e and l1 == r and l4 == t:
                            czworki.append([l3, l6, l1, l4])
                        elif l3 == w and l6 == e and l1 == r and l5 == t:
                            czworki.append([l3, l6, l1, l5])
                        elif l3 == w and l6 == e and l2 == r and l1 == t:
                            czworki.append([l3, l6, l2, l1])
                        elif l3 == w and l6 == e and l2 == r and l4 == t:
                            czworki.append([l3, l6, l2, l4])
                        elif l3 == w and l6 == e and l2 == r and l5 == t:
                            czworki.append([l3, l6, l2, l5])
                        elif l3 == w and l6 == e and l4 == r and l1 == t:
                            czworki.append([l3, l6, l4, l1])
                        elif l3 == w and l6 == e and l4 == r and l2 == t:
                            czworki.append([l3, l6, l4, l2])
                        elif l3 == w and l6 == e and l4 == r and l5 == t:
                            czworki.append([l3, l6, l4, l5])
                        elif l3 == w and l6 == e and l5 == r and l1 == t:
                            czworki.append([l3, l6, l5, l1])
                        elif l3 == w and l6 == e and l5 == r and l2 == t:
                            czworki.append([l3, l6, l5, l2])
                        elif l3 == w and l6 == e and l5 == r and l4 == t:
                            czworki.append([l3, l6, l5, l4])
                        elif l4 == w and l1 == e and l2 == r and l3 == t:
                            czworki.append([l4, l1, l2, l3])
                        elif l4 == w and l1 == e and l2 == r and l5 == t:
                            czworki.append([l4, l1, l2, l5])
                        elif l4 == w and l1 == e and l2 == r and l6 == t:
                            czworki.append([l4, l1, l2, l6])
                        elif l4 == w and l1 == e and l3 == r and l2 == t:
                            czworki.append([l4, l1, l3, l2])
                        elif l4 == w and l1 == e and l3 == r and l5 == t:
                            czworki.append([l4, l1, l3, l5])
                        elif l4 == w and l1 == e and l3 == r and l6 == t:
                            czworki.append([l4, l1, l3, l6])
                        elif l4 == w and l1 == e and l5 == r and l2 == t:
                            czworki.append([l4, l1, l5, l2])
                        elif l4 == w and l1 == e and l5 == r and l3 == t:
                            czworki.append([l4, l1, l5, l3])
                        elif l4 == w and l1 == e and l5 == r and l6 == t:
                            czworki.append([l4, l1, l5, l6])
                        elif l4 == w and l1 == e and l6 == r and l2 == t:
                            czworki.append([l4, l1, l6, l2])
                        elif l4 == w and l1 == e and l6 == r and l3 == t:
                            czworki.append([l4, l1, l6, l3])
                        elif l4 == w and l1 == e and l6 == r and l5 == t:
                            czworki.append([l4, l1, l6, l5])
                        elif l4 == w and l2 == e and l1 == r and l3 == t:
                            czworki.append([l4, l2, l1, l3])
                        elif l4 == w and l2 == e and l1 == r and l5 == t:
                            czworki.append([l4, l2, l1, l5])
                        elif l4 == w and l2 == e and l1 == r and l6 == t:
                            czworki.append([l4, l2, l1, l6])
                        elif l4 == w and l2 == e and l3 == r and l1 == t:
                            czworki.append([l4, l2, l3, l1])
                        elif l4 == w and l2 == e and l3 == r and l5 == t:
                            czworki.append([l4, l2, l3, l5])
                        elif l4 == w and l2 == e and l3 == r and l6 == t:
                            czworki.append([l4, l2, l3, l6])
                        elif l4 == w and l2 == e and l5 == r and l1 == t:
                            czworki.append([l4, l2, l5, l1])
                        elif l4 == w and l2 == e and l5 == r and l3 == t:
                            czworki.append([l4, l2, l5, l3])
                        elif l4 == w and l2 == e and l5 == r and l6 == t:
                            czworki.append([l4, l2, l5, l6])
                        elif l4 == w and l2 == e and l6 == r and l1 == t:
                            czworki.append([l4, l2, l6, l1])
                        elif l4 == w and l2 == e and l6 == r and l3 == t:
                            czworki.append([l4, l2, l6, l3])
                        elif l4 == w and l2 == e and l6 == r and l5 == t:
                            czworki.append([l4, l2, l6, l5])
                        elif l4 == w and l3 == e and l1 == r and l2 == t:
                            czworki.append([l4, l3, l1, l2])
                        elif l4 == w and l3 == e and l1 == r and l5 == t:
                            czworki.append([l4, l3, l1, l5])
                        elif l4 == w and l3 == e and l1 == r and l6 == t:
                            czworki.append([l4, l3, l1, l6])
                        elif l4 == w and l3 == e and l2 == r and l1 == t:
                            czworki.append([l4, l3, l2, l1])
                        elif l4 == w and l3 == e and l2 == r and l5 == t:
                            czworki.append([l4, l3, l2, l5])
                        elif l4 == w and l3 == e and l2 == r and l6 == t:
                            czworki.append([l4, l3, l2, l6])
                        elif l4 == w and l3 == e and l5 == r and l1 == t:
                            czworki.append([l4, l3, l5, l1])
                        elif l4 == w and l3 == e and l5 == r and l2 == t:
                            czworki.append([l4, l3, l5, l2])
                        elif l4 == w and l3 == e and l5 == r and l6 == t:
                            czworki.append([l4, l3, l5, l6])
                        elif l4 == w and l3 == e and l6 == r and l1 == t:
                            czworki.append([l4, l3, l6, l1])
                        elif l4 == w and l3 == e and l6 == r and l2 == t:
                            czworki.append([l4, l3, l6, l2])
                        elif l4 == w and l3 == e and l6 == r and l5 == t:
                            czworki.append([l4, l3, l6, l5])
                        elif l4 == w and l5 == e and l1 == r and l2 == t:
                            czworki.append([l4, l5, l1, l2])
                        elif l4 == w and l5 == e and l1 == r and l3 == t:
                            czworki.append([l4, l5, l1, l3])
                        elif l4 == w and l5 == e and l1 == r and l6 == t:
                            czworki.append([l4, l5, l1, l6])
                        elif l4 == w and l5 == e and l2 == r and l1 == t:
                            czworki.append([l4, l5, l2, l1])
                        elif l4 == w and l5 == e and l2 == r and l3 == t:
                            czworki.append([l4, l5, l2, l3])
                        elif l4 == w and l5 == e and l2 == r and l6 == t:
                            czworki.append([l4, l5, l2, l6])
                        elif l4 == w and l5 == e and l3 == r and l1 == t:
                            czworki.append([l4, l5, l3, l1])
                        elif l4 == w and l5 == e and l3 == r and l2 == t:
                            czworki.append([l4, l5, l3, l2])
                        elif l4 == w and l5 == e and l3 == r and l6 == t:
                            czworki.append([l4, l5, l3, l6])
                        elif l4 == w and l5 == e and l6 == r and l1 == t:
                            czworki.append([l4, l5, l6, l1])
                        elif l4 == w and l5 == e and l6 == r and l2 == t:
                            czworki.append([l4, l5, l6, l2])
                        elif l4 == w and l5 == e and l6 == r and l3 == t:
                            czworki.append([l4, l5, l6, l3])
                        elif l4 == w and l6 == e and l1 == r and l2 == t:
                            czworki.append([l4, l6, l1, l2])
                        elif l4 == w and l6 == e and l1 == r and l3 == t:
                            czworki.append([l4, l6, l1, l3])
                        elif l4 == w and l6 == e and l1 == r and l5 == t:
                            czworki.append([l4, l6, l1, l5])
                        elif l4 == w and l6 == e and l2 == r and l1 == t:
                            czworki.append([l4, l6, l2, l1])
                        elif l4 == w and l6 == e and l2 == r and l3 == t:
                            czworki.append([l4, l6, l2, l3])
                        elif l4 == w and l6 == e and l2 == r and l5 == t:
                            czworki.append([l4, l6, l2, l5])
                        elif l4 == w and l6 == e and l3 == r and l1 == t:
                            czworki.append([l4, l6, l3, l1])
                        elif l4 == w and l6 == e and l3 == r and l2 == t:
                            czworki.append([l4, l6, l3, l2])
                        elif l4 == w and l6 == e and l3 == r and l5 == t:
                            czworki.append([l4, l6, l3, l5])
                        elif l4 == w and l6 == e and l5 == r and l1 == t:
                            czworki.append([l4, l6, l5, l1])
                        elif l4 == w and l6 == e and l5 == r and l2 == t:
                            czworki.append([l4, l6, l5, l2])
                        elif l4 == w and l6 == e and l5 == r and l3 == t:
                            czworki.append([l4, l6, l5, l3])
                        elif l5 == w and l1 == e and l2 == r and l3 == t:
                            czworki.append([l5, l1, l2, l3])
                        elif l5 == w and l1 == e and l2 == r and l4 == t:
                            czworki.append([l5, l1, l2, l4])
                        elif l5 == w and l1 == e and l2 == r and l6 == t:
                            czworki.append([l5, l1, l2, l6])
                        elif l5 == w and l1 == e and l3 == r and l2 == t:
                            czworki.append([l5, l1, l3, l2])
                        elif l5 == w and l1 == e and l3 == r and l4 == t:
                            czworki.append([l5, l1, l3, l4])
                        elif l5 == w and l1 == e and l3 == r and l6 == t:
                            czworki.append([l5, l1, l3, l6])
                        elif l5 == w and l1 == e and l4 == r and l2 == t:
                            czworki.append([l5, l1, l4, l2])
                        elif l5 == w and l1 == e and l4 == r and l3 == t:
                            czworki.append([l5, l1, l4, l3])
                        elif l5 == w and l1 == e and l4 == r and l6 == t:
                            czworki.append([l5, l1, l4, l6])
                        elif l5 == w and l1 == e and l6 == r and l2 == t:
                            czworki.append([l5, l1, l6, l2])
                        elif l5 == w and l1 == e and l6 == r and l3 == t:
                            czworki.append([l5, l1, l6, l3])
                        elif l5 == w and l1 == e and l6 == r and l4 == t:
                            czworki.append([l5, l1, l6, l4])
                        elif l5 == w and l2 == e and l1 == r and l3 == t:
                            czworki.append([l5, l2, l1, l3])
                        elif l5 == w and l2 == e and l1 == r and l4 == t:
                            czworki.append([l5, l2, l1, l4])
                        elif l5 == w and l2 == e and l1 == r and l6 == t:
                            czworki.append([l5, l2, l1, l6])
                        elif l5 == w and l2 == e and l3 == r and l1 == t:
                            czworki.append([l5, l2, l3, l1])
                        elif l5 == w and l2 == e and l3 == r and l4 == t:
                            czworki.append([l5, l2, l3, l4])
                        elif l5 == w and l2 == e and l3 == r and l6 == t:
                            czworki.append([l5, l2, l3, l6])
                        elif l5 == w and l2 == e and l4 == r and l1 == t:
                            czworki.append([l5, l2, l4, l1])
                        elif l5 == w and l2 == e and l4 == r and l3 == t:
                            czworki.append([l5, l2, l4, l3])
                        elif l5 == w and l2 == e and l4 == r and l6 == t:
                            czworki.append([l5, l2, l4, l6])
                        elif l5 == w and l2 == e and l6 == r and l1 == t:
                            czworki.append([l5, l2, l6, l1])
                        elif l5 == w and l2 == e and l6 == r and l3 == t:
                            czworki.append([l5, l2, l6, l3])
                        elif l5 == w and l2 == e and l6 == r and l4 == t:
                            czworki.append([l5, l2, l6, l4])
                        elif l5 == w and l3 == e and l1 == r and l2 == t:
                            czworki.append([l5, l3, l1, l2])
                        elif l5 == w and l3 == e and l1 == r and l4 == t:
                            czworki.append([l5, l3, l1, l4])
                        elif l5 == w and l3 == e and l1 == r and l6 == t:
                            czworki.append([l5, l3, l1, l6])
                        elif l5 == w and l3 == e and l2 == r and l1 == t:
                            czworki.append([l5, l3, l2, l1])
                        elif l5 == w and l3 == e and l2 == r and l4 == t:
                            czworki.append([l5, l3, l2, l4])
                        elif l5 == w and l3 == e and l2 == r and l6 == t:
                            czworki.append([l5, l3, l2, l6])
                        elif l5 == w and l3 == e and l4 == r and l1 == t:
                            czworki.append([l5, l3, l4, l1])
                        elif l5 == w and l3 == e and l4 == r and l2 == t:
                            czworki.append([l5, l3, l4, l2])
                        elif l5 == w and l3 == e and l4 == r and l6 == t:
                            czworki.append([l5, l3, l4, l6])
                        elif l5 == w and l3 == e and l6 == r and l1 == t:
                            czworki.append([l5, l3, l6, l1])
                        elif l5 == w and l3 == e and l6 == r and l2 == t:
                            czworki.append([l5, l3, l6, l2])
                        elif l5 == w and l3 == e and l6 == r and l4 == t:
                            czworki.append([l5, l3, l6, l4])
                        elif l5 == w and l4 == e and l1 == r and l2 == t:
                            czworki.append([l5, l4, l1, l2])
                        elif l5 == w and l4 == e and l1 == r and l3 == t:
                            czworki.append([l5, l4, l1, l3])
                        elif l5 == w and l4 == e and l1 == r and l6 == t:
                            czworki.append([l5, l4, l1, l6])
                        elif l5 == w and l4 == e and l2 == r and l1 == t:
                            czworki.append([l5, l4, l2, l1])
                        elif l5 == w and l4 == e and l2 == r and l3 == t:
                            czworki.append([l5, l4, l2, l3])
                        elif l5 == w and l4 == e and l2 == r and l6 == t:
                            czworki.append([l5, l4, l2, l6])
                        elif l5 == w and l4 == e and l3 == r and l1 == t:
                            czworki.append([l5, l4, l3, l1])
                        elif l5 == w and l4 == e and l3 == r and l2 == t:
                            czworki.append([l5, l4, l3, l2])
                        elif l5 == w and l4 == e and l3 == r and l6 == t:
                            czworki.append([l5, l4, l3, l6])
                        elif l5 == w and l4 == e and l6 == r and l1 == t:
                            czworki.append([l5, l4, l6, l1])
                        elif l5 == w and l4 == e and l6 == r and l2 == t:
                            czworki.append([l5, l4, l6, l2])
                        elif l5 == w and l4 == e and l6 == r and l3 == t:
                            czworki.append([l5, l4, l6, l3])
                        elif l5 == w and l6 == e and l1 == r and l2 == t:
                            czworki.append([l5, l6, l1, l2])
                        elif l5 == w and l6 == e and l1 == r and l3 == t:
                            czworki.append([l5, l6, l1, l3])
                        elif l5 == w and l6 == e and l1 == r and l4 == t:
                            czworki.append([l5, l6, l1, l4])
                        elif l5 == w and l6 == e and l2 == r and l1 == t:
                            czworki.append([l5, l6, l2, l1])
                        elif l5 == w and l6 == e and l2 == r and l3 == t:
                            czworki.append([l5, l6, l2, l3])
                        elif l5 == w and l6 == e and l2 == r and l4 == t:
                            czworki.append([l5, l6, l2, l4])
                        elif l5 == w and l6 == e and l3 == r and l1 == t:
                            czworki.append([l5, l6, l3, l1])
                        elif l5 == w and l6 == e and l3 == r and l2 == t:
                            czworki.append([l5, l6, l3, l2])
                        elif l5 == w and l6 == e and l3 == r and l4 == t:
                            czworki.append([l5, l6, l3, l4])
                        elif l5 == w and l6 == e and l4 == r and l1 == t:
                            czworki.append([l5, l6, l4, l1])
                        elif l5 == w and l6 == e and l4 == r and l2 == t:
                            czworki.append([l5, l6, l4, l2])
                        elif l5 == w and l6 == e and l4 == r and l3 == t:
                            czworki.append([l5, l6, l4, l3])
                        elif l6 == w and l1 == e and l2 == r and l3 == t:
                            czworki.append([l6, l1, l2, l3])
                        elif l6 == w and l1 == e and l2 == r and l4 == t:
                            czworki.append([l6, l1, l2, l4])
                        elif l6 == w and l1 == e and l2 == r and l5 == t:
                            czworki.append([l6, l1, l2, l5])
                        elif l6 == w and l1 == e and l3 == r and l2 == t:
                            czworki.append([l6, l1, l3, l2])
                        elif l6 == w and l1 == e and l3 == r and l4 == t:
                            czworki.append([l6, l1, l3, l4])
                        elif l6 == w and l1 == e and l3 == r and l5 == t:
                            czworki.append([l6, l1, l3, l5])
                        elif l6 == w and l1 == e and l4 == r and l2 == t:
                            czworki.append([l6, l1, l4, l2])
                        elif l6 == w and l1 == e and l4 == r and l3 == t:
                            czworki.append([l6, l1, l4, l3])
                        elif l6 == w and l1 == e and l4 == r and l5 == t:
                            czworki.append([l6, l1, l4, l5])
                        elif l6 == w and l1 == e and l5 == r and l2 == t:
                            czworki.append([l6, l1, l5, l2])
                        elif l6 == w and l1 == e and l5 == r and l3 == t:
                            czworki.append([l6, l1, l5, l3])
                        elif l6 == w and l1 == e and l5 == r and l4 == t:
                            czworki.append([l6, l1, l5, l4])
                        elif l6 == w and l2 == e and l1 == r and l3 == t:
                            czworki.append([l6, l2, l1, l3])
                        elif l6 == w and l2 == e and l1 == r and l4 == t:
                            czworki.append([l6, l2, l1, l4])
                        elif l6 == w and l2 == e and l1 == r and l5 == t:
                            czworki.append([l6, l2, l1, l5])
                        elif l6 == w and l2 == e and l3 == r and l1 == t:
                            czworki.append([l6, l2, l3, l1])
                        elif l6 == w and l2 == e and l3 == r and l4 == t:
                            czworki.append([l6, l2, l3, l4])
                        elif l6 == w and l2 == e and l3 == r and l5 == t:
                            czworki.append([l6, l2, l3, l5])
                        elif l6 == w and l2 == e and l4 == r and l1 == t:
                            czworki.append([l6, l2, l4, l1])
                        elif l6 == w and l2 == e and l4 == r and l3 == t:
                            czworki.append([l6, l2, l4, l3])
                        elif l6 == w and l2 == e and l4 == r and l5 == t:
                            czworki.append([l6, l2, l4, l5])
                        elif l6 == w and l2 == e and l5 == r and l1 == t:
                            czworki.append([l6, l2, l5, l1])
                        elif l6 == w and l2 == e and l5 == r and l3 == t:
                            czworki.append([l6, l2, l5, l3])
                        elif l6 == w and l2 == e and l5 == r and l4 == t:
                            czworki.append([l6, l2, l5, l4])
                        elif l6 == w and l3 == e and l1 == r and l2 == t:
                            czworki.append([l6, l3, l1, l2])
                        elif l6 == w and l3 == e and l1 == r and l4 == t:
                            czworki.append([l6, l3, l1, l4])
                        elif l6 == w and l3 == e and l1 == r and l5 == t:
                            czworki.append([l6, l3, l1, l5])
                        elif l6 == w and l3 == e and l2 == r and l1 == t:
                            czworki.append([l6, l3, l2, l1])
                        elif l6 == w and l3 == e and l2 == r and l4 == t:
                            czworki.append([l6, l3, l2, l4])
                        elif l6 == w and l3 == e and l2 == r and l5 == t:
                            czworki.append([l6, l3, l2, l5])
                        elif l6 == w and l3 == e and l4 == r and l1 == t:
                            czworki.append([l6, l3, l4, l1])
                        elif l6 == w and l3 == e and l4 == r and l2 == t:
                            czworki.append([l6, l3, l4, l2])
                        elif l6 == w and l3 == e and l4 == r and l5 == t:
                            czworki.append([l6, l3, l4, l5])
                        elif l6 == w and l3 == e and l5 == r and l1 == t:
                            czworki.append([l6, l3, l5, l1])
                        elif l6 == w and l3 == e and l5 == r and l2 == t:
                            czworki.append([l6, l3, l5, l2])
                        elif l6 == w and l3 == e and l5 == r and l4 == t:
                            czworki.append([l6, l3, l5, l4])
                        elif l6 == w and l4 == e and l1 == r and l2 == t:
                            czworki.append([l6, l4, l1, l2])
                        elif l6 == w and l4 == e and l1 == r and l3 == t:
                            czworki.append([l6, l4, l1, l3])
                        elif l6 == w and l4 == e and l1 == r and l5 == t:
                            czworki.append([l6, l4, l1, l5])
                        elif l6 == w and l4 == e and l2 == r and l1 == t:
                            czworki.append([l6, l4, l2, l1])
                        elif l6 == w and l4 == e and l2 == r and l3 == t:
                            czworki.append([l6, l4, l2, l3])
                        elif l6 == w and l4 == e and l2 == r and l5 == t:
                            czworki.append([l6, l4, l2, l5])
                        elif l6 == w and l4 == e and l3 == r and l1 == t:
                            czworki.append([l6, l4, l3, l1])
                        elif l6 == w and l4 == e and l3 == r and l2 == t:
                            czworki.append([l6, l4, l3, l2])
                        elif l6 == w and l4 == e and l3 == r and l5 == t:
                            czworki.append([l6, l4, l3, l5])
                        elif l6 == w and l4 == e and l5 == r and l1 == t:
                            czworki.append([l6, l4, l5, l1])
                        elif l6 == w and l4 == e and l5 == r and l2 == t:
                            czworki.append([l6, l4, l5, l2])
                        elif l6 == w and l4 == e and l5 == r and l3 == t:
                            czworki.append([l6, l4, l5, l3])
                        elif l6 == w and l5 == e and l1 == r and l2 == t:
                            czworki.append([l6, l5, l1, l2])
                        elif l6 == w and l5 == e and l1 == r and l3 == t:
                            czworki.append([l6, l5, l1, l3])
                        elif l6 == w and l5 == e and l1 == r and l4 == t:
                            czworki.append([l6, l5, l1, l4])
                        elif l6 == w and l5 == e and l2 == r and l1 == t:
                            czworki.append([l6, l5, l2, l1])
                        elif l6 == w and l5 == e and l2 == r and l3 == t:
                            czworki.append([l6, l5, l2, l3])
                        elif l6 == w and l5 == e and l2 == r and l4 == t:
                            czworki.append([l6, l5, l2, l4])
                        elif l6 == w and l5 == e and l3 == r and l1 == t:
                            czworki.append([l6, l5, l3, l1])
                        elif l6 == w and l5 == e and l3 == r and l2 == t:
                            czworki.append([l6, l5, l3, l2])
                        elif l6 == w and l5 == e and l3 == r and l4 == t:
                            czworki.append([l6, l5, l3, l4])
                        elif l6 == w and l5 == e and l4 == r and l1 == t:
                            czworki.append([l6, l5, l4, l1])
                        elif l6 == w and l5 == e and l4 == r and l2 == t:
                            czworki.append([l6, l5, l4, l2])
                        elif l6 == w and l5 == e and l4 == r and l3 == t:
                            czworki.append([l6, l5, l4, l3])

        conn.close()
        czworki.sort()
        liczbaTrojek = len(czworki)

        listaCz = []
        for r in range(1, 50):
            for t in range(1, 50):
                for y in range(1, 50):
                    for u in range(1, 50):
                        licznik = czworki.count([r, t, y, u])
                        listaCz.append([licznik, r, t, y, u])

        listaCz.sort()

        r = len(listaCz)
        r = r-1
        t = r-20
        ypolozenie = 10
        for i in range(r, t, -1):
            losowanie = (listaCz[r][0])
            liczbaPara1 = (listaCz[r][1])
            liczbaPara2 = (listaCz[r][2])
            liczbaPara3 = (listaCz[r][3])
            liczbaPara4 = (listaCz[r][4])
            r -= 1

            tk.Label(self.ramka1, text="("+str(liczbaPara1)+" - "+str(liczbaPara2) + " - "+str(liczbaPara3) +
                     " - "+str(liczbaPara4)+")", font=("Arial", 12), bg="#ADD8E6").place(x=40, y=ypolozenie)
            tk.Label(self.ramka1, text="--- "+str(losowanie)+" razy",
                     font=("Arial", 12), bg="#ADD8E6").place(x=170, y=ypolozenie)

            ypolozenie += 25

        r = len(listaCz)
        r = r-21
        t = r-20
        ypolozenie = 10
        for i in range(r, t, -1):
            losowanie = (listaCz[r][0])
            liczbaPara1 = (listaCz[r][1])
            liczbaPara2 = (listaCz[r][2])
            liczbaPara3 = (listaCz[r][3])
            liczbaPara4 = (listaCz[r][4])
            r -= 1

            tk.Label(self.ramka1, text="("+str(liczbaPara1)+" - "+str(liczbaPara2) + " - "+str(liczbaPara3) +
                     " - "+str(liczbaPara4)+")", font=("Arial", 12), bg="#ADD8E6").place(x=390, y=ypolozenie)
            tk.Label(self.ramka1, text="--- "+str(losowanie)+" razy",
                     font=("Arial", 12), bg="#ADD8E6").place(x=520, y=ypolozenie)
            ypolozenie += 25

        but = tk.Button(self.ramka1, text="zamknij to okno",
                        bg="#DC143C", command=self.zamknij_okno)
        but.place(x=320, y=540)


# definicja analizy trojek


    def analiza_trojek(self):
        self.ramka1 = Frame(root,  height=596, width=650, bg="#ADD8E6")
        self.ramka1.pack(padx=5, pady=5, side=RIGHT)
        trojki = []

        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lotto")
        records = c.fetchall()
        for rec in records:
            l1 = str(rec[3])
            l1 = int(l1)

            l2 = str(rec[4])
            l2 = int(l2)

            l3 = str(rec[5])
            l3 = int(l3)

            l4 = str(rec[6])
            l4 = int(l4)

            l5 = str(rec[7])
            l5 = int(l5)

            l6 = str(rec[8])
            l6 = int(l6)

        for q in range(1, 50):
            for w in range(1, 50):
                for e in range(1, 50):
                    if l1 == q and l2 == w and l3 == e:
                        trojki.append([l1, l2, l3])
                    elif l1 == q and l2 == w and l4 == e:
                        trojki.append([l1, l2, l4])
                    elif l1 == q and l2 == w and l5 == e:
                        trojki.append([l1, l2, l5])
                    elif l1 == q and l2 == w and l6 == e:
                        trojki.append([l1, l2, l6])

                    elif l1 == q and l3 == w and l2 == e:
                        trojki.append([l1, l3, l2])
                    elif l1 == q and l3 == w and l4 == e:
                        trojki.append([l1, l3, l4])
                    elif l1 == q and l3 == w and l5 == e:
                        trojki.append([l1, l3, l6])
                    elif l1 == q and l3 == w and l6 == e:
                        trojki.append([l1, l3, l6])

                    elif l1 == q and l4 == w and l2 == e:
                        trojki.append([l1, l4, l2])
                    elif l1 == q and l4 == w and l3 == e:
                        trojki.append([l1, l4, l3])
                    elif l1 == q and l4 == w and l5 == e:
                        trojki.append([l1, l4, l5])
                    elif l1 == q and l4 == w and l6 == e:
                        trojki.append([l1, l4, l6])

                    elif l1 == q and l5 == w and l2 == e:
                        trojki.append([l1, l5, l2])
                    elif l1 == q and l5 == w and l3 == e:
                        trojki.append([l1, l5, l3])
                    elif l1 == q and l5 == w and l4 == e:
                        trojki.append([l1, l5, l4])
                    elif l1 == q and l5 == w and l6 == e:
                        trojki.append([l1, l5, l6])

                    elif l1 == q and l6 == w and l2 == e:
                        trojki.append([l1, l6, l2])
                    elif l1 == q and l6 == w and l3 == e:
                        trojki.append([l1, l6, l3])
                    elif l1 == q and l6 == w and l4 == e:
                        trojki.append([l1, l6, l4])
                    elif l1 == q and l6 == w and l5 == e:
                        trojki.append([l1, l6, l5])

                    elif l2 == q and l1 == w and l3 == e:
                        trojki.append([l2, l1, l3])
                    elif l2 == q and l1 == w and l4 == e:
                        trojki.append([l2, l1, l4])
                    elif l2 == q and l1 == w and l5 == e:
                        trojki.append([l2, l1, l5])
                    elif l2 == q and l1 == w and l6 == e:
                        trojki.append([l2, l1, l6])

                    elif l2 == q and l3 == w and l1 == e:
                        trojki.append([l2, l3, l1])
                    elif l2 == q and l3 == w and l4 == e:
                        trojki.append([l2, l3, l4])
                    elif l2 == q and l3 == w and l5 == e:
                        trojki.append([l2, l3, l5])
                    elif l2 == q and l3 == w and l6 == e:
                        trojki.append([l2, l3, l6])

                    elif l2 == q and l4 == w and l1 == e:
                        trojki.append([l2, l4, l1])
                    elif l2 == q and l4 == w and l3 == e:
                        trojki.append([l2, l4, l3])
                    elif l2 == q and l4 == w and l5 == e:
                        trojki.append([l2, l4, l5])
                    elif l2 == q and l4 == w and l6 == e:
                        trojki.append([l2, l4, l6])

                    elif l2 == q and l5 == w and l1 == e:
                        trojki.append([l2, l5, l1])
                    elif l2 == q and l5 == w and l3 == e:
                        trojki.append([l2, l5, l3])
                    elif l2 == q and l5 == w and l4 == e:
                        trojki.append([l2, l5, l4])
                    elif l2 == q and l5 == w and l6 == e:
                        trojki.append([l2, l5, l6])

                    elif l2 == q and l6 == w and l1 == e:
                        trojki.append([l2, l6, l1])
                    elif l2 == q and l6 == w and l3 == e:
                        trojki.append([l2, l6, l3])
                    elif l2 == q and l6 == w and l4 == e:
                        trojki.append([l2, l6, l4])
                    elif l2 == q and l6 == w and l5 == e:
                        trojki.append([l2, l6, l5])

                    elif l3 == q and l1 == w and l2 == e:
                        trojki.append([l3, l1, l2])
                    elif l3 == q and l1 == w and l4 == e:
                        trojki.append([l3, l1, l4])
                    elif l3 == q and l1 == w and l5 == e:
                        trojki.append([l3, l1, l5])
                    elif l3 == q and l1 == w and l6 == e:
                        trojki.append([l3, l1, l6])

                    elif l3 == q and l2 == w and l1 == e:
                        trojki.append([l3, l2, l1])
                    elif l3 == q and l2 == w and l4 == e:
                        trojki.append([l3, l2, l4])
                    elif l3 == q and l2 == w and l5 == e:
                        trojki.append([l3, l2, l5])
                    elif l3 == q and l2 == w and l6 == e:
                        trojki.append([l3, l2, l6])

                    elif l3 == q and l4 == w and l1 == e:
                        trojki.append([l3, l4, l1])
                    elif l3 == q and l4 == w and l2 == e:
                        trojki.append([l3, l4, l2])
                    elif l3 == q and l4 == w and l5 == e:
                        trojki.append([l3, l4, l5])
                    elif l3 == q and l4 == w and l6 == e:
                        trojki.append([l3, l4, l6])

                    elif l3 == q and l5 == w and l1 == e:
                        trojki.append([l3, l5, l1])
                    elif l3 == q and l5 == w and l2 == e:
                        trojki.append([l3, l5, l2])
                    elif l3 == q and l5 == w and l4 == e:
                        trojki.append([l3, l5, l4])
                    elif l3 == q and l5 == w and l6 == e:
                        trojki.append([l3, l5, l6])

                    elif l3 == q and l6 == w and l1 == e:
                        trojki.append([l3, l6, l1])
                    elif l3 == q and l6 == w and l2 == e:
                        trojki.append([l3, l6, l2])
                    elif l3 == q and l6 == w and l4 == e:
                        trojki.append([l3, l6, l4])
                    elif l3 == q and l6 == w and l5 == e:
                        trojki.append([l3, l6, l5])

                    elif l4 == q and l1 == w and l1 == e:
                        trojki.append([l4, l1, l1])
                    elif l4 == q and l1 == w and l2 == e:
                        trojki.append([l4, l1, l2])
                    elif l4 == q and l1 == w and l5 == e:
                        trojki.append([l4, l1, l5])
                    elif l4 == q and l1 == w and l6 == e:
                        trojki.append([l4, l1, l6])

                    elif l4 == q and l2 == w and l1 == e:
                        trojki.append([l4, l2, l1])
                    elif l4 == q and l2 == w and l3 == e:
                        trojki.append([l4, l2, l3])
                    elif l4 == q and l2 == w and l5 == e:
                        trojki.append([l4, l2, l5])
                    elif l4 == q and l2 == w and l6 == e:
                        trojki.append([l4, l2, l6])

                    elif l4 == q and l3 == w and l1 == e:
                        trojki.append([l4, l3, l1])
                    elif l4 == q and l3 == w and l2 == e:
                        trojki.append([l4, l3, l2])
                    elif l4 == q and l3 == w and l5 == e:
                        trojki.append([l4, l3, l5])
                    elif l4 == q and l3 == w and l6 == e:
                        trojki.append([l4, l3, l6])

                    elif l4 == q and l5 == w and l1 == e:
                        trojki.append([l4, l5, l1])
                    elif l4 == q and l5 == w and l2 == e:
                        trojki.append([l4, l5, l2])
                    elif l4 == q and l5 == w and l3 == e:
                        trojki.append([l4, l5, l3])
                    elif l4 == q and l5 == w and l6 == e:
                        trojki.append([l4, l5, l6])

                    elif l4 == q and l6 == w and l1 == e:
                        trojki.append([l4, l6, l1])
                    elif l4 == q and l6 == w and l2 == e:
                        trojki.append([l4, l6, l2])
                    elif l4 == q and l6 == w and l3 == e:
                        trojki.append([l4, l6, l3])
                    elif l4 == q and l6 == w and l5 == e:
                        trojki.append([l4, l6, l5])

                    elif l5 == q and l1 == w and l2 == e:
                        trojki.append([l5, l1, l2])
                    elif l5 == q and l1 == w and l3 == e:
                        trojki.append([l5, l1, l3])
                    elif l5 == q and l1 == w and l4 == e:
                        trojki.append([l5, l1, l4])
                    elif l5 == q and l1 == w and l6 == e:
                        trojki.append([l5, l1, l6])

                    elif l5 == q and l2 == w and l1 == e:
                        trojki.append([l5, l2, l1])
                    elif l5 == q and l2 == w and l3 == e:
                        trojki.append([l5, l2, l3])
                    elif l5 == q and l2 == w and l4 == e:
                        trojki.append([l5, l2, l4])
                    elif l5 == q and l2 == w and l6 == e:
                        trojki.append([l5, l2, l6])

                    elif l5 == q and l3 == w and l1 == e:
                        trojki.append([l5, l3, l1])
                    elif l5 == q and l3 == w and l2 == e:
                        trojki.append([l5, l3, l2])
                    elif l5 == q and l3 == w and l4 == e:
                        trojki.append([l5, l3, l4])
                    elif l5 == q and l3 == w and l6 == e:
                        trojki.append([l5, l3, l6])

                    elif l5 == q and l4 == w and l1 == e:
                        trojki.append([l5, l4, l1])
                    elif l5 == q and l4 == w and l2 == e:
                        trojki.append([l5, l4, l2])
                    elif l5 == q and l4 == w and l3 == e:
                        trojki.append([l5, l4, l3])
                    elif l5 == q and l4 == w and l6 == e:
                        trojki.append([l5, l4, l6])

                    elif l5 == q and l6 == w and l1 == e:
                        trojki.append([l5, l6, l1])
                    elif l5 == q and l6 == w and l2 == e:
                        trojki.append([l5, l6, l2])
                    elif l5 == q and l6 == w and l3 == e:
                        trojki.append([l5, l6, l3])
                    elif l5 == q and l6 == w and l4 == e:
                        trojki.append([l5, l6, l4])

                    elif l6 == q and l1 == w and l2 == e:
                        trojki.append([l6, l1, l2])
                    elif l6 == q and l1 == w and l3 == e:
                        trojki.append([l6, l1, l3])
                    elif l6 == q and l1 == w and l4 == e:
                        trojki.append([l6, l1, l4])
                    elif l6 == q and l1 == w and l5 == e:
                        trojki.append([l6, l1, l5])

                    elif l6 == q and l2 == w and l1 == e:
                        trojki.append([l6, l2, l1])
                    elif l6 == q and l2 == w and l3 == e:
                        trojki.append([l6, l2, l3])
                    elif l6 == q and l2 == w and l4 == e:
                        trojki.append([l6, l2, l4])
                    elif l6 == q and l2 == w and l5 == e:
                        trojki.append([l6, l2, l5])

                    elif l6 == q and l3 == w and l1 == e:
                        trojki.append([l6, l3, l1])
                    elif l6 == q and l3 == w and l2 == e:
                        trojki.append([l6, l3, l2])
                    elif l6 == q and l3 == w and l4 == e:
                        trojki.append([l6, l3, l4])
                    elif l6 == q and l3 == w and l5 == e:
                        trojki.append([l6, l3, l5])

                    elif l6 == q and l4 == w and l1 == e:
                        trojki.append([l6, l4, l1])
                    elif l6 == q and l4 == w and l2 == e:
                        trojki.append([l6, l4, l2])
                    elif l6 == q and l4 == w and l3 == e:
                        trojki.append([l6, l4, l3])
                    elif l6 == q and l4 == w and l5 == e:
                        trojki.append([l6, l4, l5])

                    elif l6 == q and l5 == w and l1 == e:
                        trojki.append([l6, l5, l1])
                    elif l6 == q and l5 == w and l2 == e:
                        trojki.append([l6, l5, l2])
                    elif l6 == q and l5 == w and l3 == e:
                        trojki.append([l6, l5, l3])
                    elif l6 == q and l5 == w and l4 == e:
                        trojki.append([l4, l5, l4])

        conn.close()
        trojki.sort()
        liczbaTrojek = len(trojki)

        listaT = []
        for r in range(1, 50):
            for t in range(1, 50):
                for y in range(1, 50):
                    licznik = trojki.count([r, t, y])
                    listaT.append([licznik, r, t, y])

        listaT.sort()

        r = len(listaT)
        r = r-1
        t = r-20
        ypolozenie = 10
        for i in range(r, t, -1):
            losowanie = (listaT[r][0])
            liczbaPara1 = (listaT[r][1])
            liczbaPara2 = (listaT[r][2])
            liczbaPara3 = (listaT[r][3])
            r -= 1

            tk.Label(self.ramka1, text="("+str(liczbaPara1)+" - "+str(liczbaPara2) + " - " +
                     str(liczbaPara3)+")", font=("Arial", 12), bg="#ADD8E6").place(x=40, y=ypolozenie)
            tk.Label(self.ramka1, text="--- "+str(losowanie)+" razy",
                     font=("Arial", 12), bg="#ADD8E6").place(x=140, y=ypolozenie)
            ypolozenie += 25

        r = len(listaT)
        r = r-21
        t = r-20
        ypolozenie = 10
        for i in range(r, t, -1):
            losowanie = (listaT[r][0])
            liczbaPara1 = (listaT[r][1])
            liczbaPara2 = (listaT[r][2])
            liczbaPara3 = (listaT[r][3])
            r -= 1

            tk.Label(self.ramka1, text="("+str(liczbaPara1)+" - "+str(liczbaPara2) + " - " +
                     str(liczbaPara3)+")", font=("Arial", 12), bg="#ADD8E6").place(x=240, y=ypolozenie)
            tk.Label(self.ramka1, text="--- "+str(losowanie)+" razy",
                     font=("Arial", 12), bg="#ADD8E6").place(x=340, y=ypolozenie)
            ypolozenie += 25

        r = len(listaT)
        r = r-41
        t = r-20
        ypolozenie = 10
        for i in range(r, t, -1):
            losowanie = (listaT[r][0])
            liczbaPara1 = (listaT[r][1])
            liczbaPara2 = (listaT[r][2])
            liczbaPara3 = (listaT[r][3])
            r -= 1

            tk.Label(self.ramka1, text="("+str(liczbaPara1)+" - "+str(liczbaPara2) + " - " +
                     str(liczbaPara3)+")", font=("Arial", 12), bg="#ADD8E6").place(x=440, y=ypolozenie)
            tk.Label(self.ramka1, text="--- "+str(losowanie)+" razy",
                     font=("Arial", 12), bg="#ADD8E6").place(x=540, y=ypolozenie)
            ypolozenie += 25

        but = tk.Button(self.ramka1, text="zamknij to okno",
                        bg="#DC143C", command=self.zamknij_okno)
        but.place(x=320, y=540)


# definicja analizy par

    def analiza_par(self):
        self.ramka1 = Frame(root,  height=596, width=650, bg="#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side=RIGHT)

        pary = []

        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lotto")
        records = c.fetchall()
        for rec in records:
            liczba_1 = str(rec[3])
            liczba_1 = int(liczba_1)

            liczba_2 = str(rec[4])
            liczba_2 = int(liczba_2)

            liczba_3 = str(rec[5])
            liczba_3 = int(liczba_3)

            liczba_4 = str(rec[6])
            liczba_4 = int(liczba_4)

            liczba_5 = str(rec[7])
            liczba_5 = int(liczba_5)

            liczba_6 = str(rec[8])
            liczba_6 = int(liczba_6)

            for i in range(1, 50):
                for j in range(1, 50):
                    if liczba_1 == i and liczba_2 == j:
                        pary.append([liczba_1, liczba_2])
                    elif liczba_1 == i and liczba_3 == j:
                        pary.append([liczba_1, liczba_3])
                    elif liczba_1 == i and liczba_4 == j:
                        pary.append([liczba_1, liczba_4])
                    elif liczba_1 == i and liczba_5 == j:
                        pary.append([liczba_1, liczba_5])
                    elif liczba_1 == i and liczba_6 == j:
                        pary.append([liczba_1, liczba_6])

                    elif liczba_2 == i and liczba_1 == j:
                        pary.append([liczba_2, liczba_1])
                    elif liczba_2 == i and liczba_3 == j:
                        pary.append([liczba_2, liczba_3])
                    elif liczba_2 == i and liczba_4 == j:
                        pary.append([liczba_2, liczba_4])
                    elif liczba_2 == i and liczba_5 == j:
                        pary.append([liczba_2, liczba_5])
                    elif liczba_2 == i and liczba_6 == j:
                        pary.append([liczba_2, liczba_6])

                    elif liczba_3 == i and liczba_1 == j:
                        pary.append([liczba_3, liczba_1])
                    elif liczba_3 == i and liczba_2 == j:
                        pary.append([liczba_3, liczba_2])
                    elif liczba_3 == i and liczba_4 == j:
                        pary.append([liczba_3, liczba_4])
                    elif liczba_3 == i and liczba_5 == j:
                        pary.append([liczba_3, liczba_5])
                    elif liczba_3 == i and liczba_6 == j:
                        pary.append([liczba_3, liczba_6])

                    elif liczba_4 == i and liczba_1 == j:
                        pary.append([liczba_4, liczba_1])
                    elif liczba_4 == i and liczba_2 == j:
                        pary.append([liczba_4, liczba_2])
                    elif liczba_4 == i and liczba_3 == j:
                        pary.append([liczba_4, liczba_3])
                    elif liczba_4 == i and liczba_5 == j:
                        pary.append([liczba_4, liczba_5])
                    elif liczba_4 == i and liczba_6 == j:
                        pary.append([liczba_4, liczba_6])

                    elif liczba_5 == i and liczba_1 == j:
                        pary.append([liczba_5, liczba_1])
                    elif liczba_5 == i and liczba_2 == j:
                        pary.append([liczba_5, liczba_2])
                    elif liczba_5 == i and liczba_3 == j:
                        pary.append([liczba_5, liczba_3])
                    elif liczba_5 == i and liczba_4 == j:
                        pary.append([liczba_5, liczba_4])
                    elif liczba_5 == i and liczba_6 == j:
                        pary.append([liczba_5, liczba_6])

        conn.close()
        pary.sort()
        liczbaPary = len(pary)

        listaP = []
        for r in range(1, 50):
            for t in range(1, 50):
                licznik = pary.count([r, t])
                listaP.append([licznik, r, t])

        listaP.sort()
        r = len(listaP)
        r = r-1
        t = r-20
        ypolozenie = 10
        for i in range(r, t, -1):
            losowanie = (listaP[r][0])
            liczbaPara1 = (listaP[r][1])
            liczbaPara2 = (listaP[r][2])
            r -= 1

            tk.Label(self.ramka1, text="("+str(liczbaPara1)+" - "+str(liczbaPara2) + ")",
                     font=("Arial", 12), bg="#FAFAD2").place(x=40, y=ypolozenie)
            tk.Label(self.ramka1, text=" --- "+str(losowanie),
                     font=("Arial", 12), bg="#FAFAD2").place(x=110, y=ypolozenie)
            ypolozenie += 25

        r = len(listaP)
        r = r-21
        t = r-20
        ypolozenie = 10
        for i in range(r, t, -1):
            losowanie = (listaP[r][0])
            liczbaPara1 = (listaP[r][1])
            liczbaPara2 = (listaP[r][2])
            r -= 1

            tk.Label(self.ramka1, text="("+str(liczbaPara1)+" - "+str(liczbaPara2) + ")",
                     font=("Arial", 12), bg="#FAFAD2").place(x=240, y=ypolozenie)
            tk.Label(self.ramka1, text=" --- "+str(losowanie),
                     font=("Arial", 12), bg="#FAFAD2").place(x=310, y=ypolozenie)
            ypolozenie += 25

        r = len(listaP)
        r = r-41
        t = r-20
        ypolozenie = 10
        for i in range(r, t, -1):
            losowanie = (listaP[r][0])
            liczbaPara1 = (listaP[r][1])
            liczbaPara2 = (listaP[r][2])
            r -= 1

            tk.Label(self.ramka1, text="("+str(liczbaPara1)+" - "+str(liczbaPara2) + ")",
                     font=("Arial", 12), bg="#FAFAD2").place(x=440, y=ypolozenie)
            tk.Label(self.ramka1, text=" --- "+str(losowanie),
                     font=("Arial", 12), bg="#FAFAD2").place(x=510, y=ypolozenie)
            ypolozenie += 25

        but = tk.Button(self.ramka1, text="zamknij to okno",
                        bg="#DC143C", command=self.zamknij_okno)
        but.place(x=320, y=530)


# definicja sprawdza powtarzające się liczby


    def liczby_powtorzone(self):
        self.ramka1 = Frame(root, height=550, width=600, bg="#E9967A")
        self.ramka1.pack(padx=5, pady=5, side=TOP)

        lista = []
        liczenie = []

        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lotto")
        records = c.fetchall()
        for rec in records:
            liczba_1 = str(rec[3])
            liczba_1 = int(liczba_1)

            liczba_2 = str(rec[4])
            liczba_2 = int(liczba_2)

            liczba_3 = str(rec[5])
            liczba_3 = int(liczba_3)

            liczba_4 = str(rec[6])
            liczba_4 = int(liczba_4)

            liczba_5 = str(rec[7])
            liczba_5 = int(liczba_5)

            liczba_6 = str(rec[8])
            liczba_6 = int(liczba_6)

            lista.append(liczba_1)
            lista.append(liczba_2)
            lista.append(liczba_3)
            lista.append(liczba_4)
            lista.append(liczba_5)
            lista.append(liczba_6)

        l1 = lista.count(1)
        liczenie.append([l1, 1])
        l2 = lista.count(2)
        liczenie.append([l2, 2])
        l3 = lista.count(3)
        liczenie.append([l3, 3])
        l4 = lista.count(4)
        liczenie.append([l4, 4])
        l5 = lista.count(5)
        liczenie.append([l5, 5])
        l6 = lista.count(6)
        liczenie.append([l6, 6])
        l7 = lista.count(7)
        liczenie.append([l7, 7])
        l8 = lista.count(8)
        liczenie.append([l8, 8])
        l9 = lista.count(9)
        liczenie.append([l9, 9])
        l10 = lista.count(10)
        liczenie.append([l10, 10])

        l11 = lista.count(11)
        liczenie.append([l11, 11])
        l12 = lista.count(12)
        liczenie.append([l12, 12])
        l13 = lista.count(13)
        liczenie.append([l13, 13])
        l14 = lista.count(14)
        liczenie.append([l14, 14])
        l15 = lista.count(15)
        liczenie.append([l15, 15])
        l16 = lista.count(16)
        liczenie.append([l16, 16])
        l17 = lista.count(17)
        liczenie.append([l17, 17])
        l18 = lista.count(18)
        liczenie.append([l18, 18])
        l19 = lista.count(19)
        liczenie.append([l19, 19])
        l20 = lista.count(20)
        liczenie.append([l20, 20])

        l21 = lista.count(21)
        liczenie.append([l21, 21])
        l22 = lista.count(22)
        liczenie.append([l22, 22])
        l23 = lista.count(23)
        liczenie.append([l23, 23])
        l24 = lista.count(24)
        liczenie.append([l24, 24])
        l25 = lista.count(25)
        liczenie.append([l25, 25])
        l26 = lista.count(26)
        liczenie.append([l26, 26])
        l27 = lista.count(27)
        liczenie.append([l27, 27])
        l28 = lista.count(28)
        liczenie.append([l28, 28])
        l29 = lista.count(29)
        liczenie.append([l29, 29])
        l30 = lista.count(30)
        liczenie.append([l30, 30])

        l31 = lista.count(31)
        liczenie.append([l31, 31])
        l32 = lista.count(32)
        liczenie.append([l32, 32])
        l33 = lista.count(33)
        liczenie.append([l33, 33])
        l34 = lista.count(34)
        liczenie.append([l34, 34])
        l35 = lista.count(35)
        liczenie.append([l35, 35])
        l36 = lista.count(36)
        liczenie.append([l36, 36])
        l37 = lista.count(37)
        liczenie.append([l37, 37])
        l38 = lista.count(38)
        liczenie.append([l38, 38])
        l39 = lista.count(39)
        liczenie.append([l39, 39])
        l40 = lista.count(40)
        liczenie.append([l40, 40])

        l41 = lista.count(41)
        liczenie.append([l41, 41])
        l42 = lista.count(42)
        liczenie.append([l42, 42])
        l43 = lista.count(43)
        liczenie.append([l43, 43])
        l44 = lista.count(44)
        liczenie.append([l44, 44])
        l45 = lista.count(45)
        liczenie.append([l45, 45])
        l46 = lista.count(46)
        liczenie.append([l46, 46])
        l47 = lista.count(47)
        liczenie.append([l47, 47])
        l48 = lista.count(48)
        liczenie.append([l48, 48])
        l49 = lista.count(49)
        liczenie.append([l49, 49])

        liczenie.sort()

        conn.close()
        ypolozenie = 5
        xpolozenie = 5
        zpolozenie = 5

        for i in range(48, 30, -1):
            iloscLosowan = (liczenie[i][0])
            liczbaLosowana = (liczenie[i][1])

            tk.Label(self.ramka1, text=liczbaLosowana, font=(
                "Arial", 12), bg="green").place(x=20, y=ypolozenie)
            tk.Label(self.ramka1, text=" -- ", font=("Arial", 12),
                     bg="#E9967A").place(x=50, y=ypolozenie)
            tk.Label(self.ramka1, text=str(iloscLosowan), font=(
                "Arial", 12), bg="#FAFAD2").place(x=75, y=ypolozenie)
            ypolozenie += 27

        for j in range(30, 12, -1):
            iloscLosowan = (liczenie[j][0])
            liczbaLosowana = (liczenie[j][1])

            tk.Label(self.ramka1, text=liczbaLosowana, font=(
                "Arial", 12), bg="green").place(x=170, y=xpolozenie)
            tk.Label(self.ramka1, text=" -- ", font=("Arial", 12),
                     bg="#E9967A").place(x=200, y=xpolozenie)
            tk.Label(self.ramka1, text=str(iloscLosowan), font=(
                "Arial", 12), bg="#FAFAD2").place(x=225, y=xpolozenie)
            xpolozenie += 27

        for k in range(12, -1, -1):
            iloscLosowan = (liczenie[k][0])
            liczbaLosowana = (liczenie[k][1])

            tk.Label(self.ramka1, text=liczbaLosowana, font=(
                "Arial", 12), bg="green").place(x=320, y=zpolozenie)
            tk.Label(self.ramka1, text=" -- ", font=("Arial", 12),
                     bg="#E9967A").place(x=350, y=zpolozenie)
            tk.Label(self.ramka1, text=str(iloscLosowan), font=(
                "Arial", 12), bg="#FAFAD2").place(x=375, y=zpolozenie)
            zpolozenie += 27

        but = tk.Button(self.ramka1, text="zamknij to okno",
                        bg="#DC143C", command=self.zamknij_okno)
        but.place(x=420, y=500)


# definicja rejestracji użytkownika

    def rejestracja_usera(self):
        self.ramka1 = Frame(root,  height=180, width=600, bg="#DDA0DD")
        self.ramka1.pack(padx=5, pady=5, side=TOP)
        lab = tk.Label(self.ramka1, text="Podaj swoje imię:",
                       font=("Arial", 13), bg="#DDA0DD")
        lab.place(x=10, y=10)

        lab2 = tk.Label(self.ramka1, text="Podaj swoje nazwisko:",
                        font=("Arial", 13), bg="#DDA0DD")
        lab2.place(x=10, y=45)

        lab3 = tk.Label(self.ramka1, text="Podaj email kontaktowy",
                        font=("Arial", 13), bg="#DDA0DD")
        lab3.place(x=10, y=80)

        self.imie = StringVar()
        self.nazwisko = StringVar()
        self.email = StringVar()

        self.en = tk.Entry(
            self.ramka1, textvariable=self.imie, font=("Arial", 13))
        self.en.place(x=200, y=10)

        self.en1 = tk.Entry(
            self.ramka1, textvariable=self.nazwisko, font=("Arial", 13))
        self.en1.place(x=200, y=45)

        self.en2 = tk.Entry(
            self.ramka1, textvariable=self.email, font=("Arial", 13))
        self.en2.place(x=200, y=80)

        self.but = tk.Button(self.ramka1, text="wyczyść pola",
                             bg="#DA70D6", command=self.czyscioch)
        self.but.place(x=100, y=135)

        self.but = tk.Button(self.ramka1, text="zarejestrój",
                             fg="white", bg="#800080", command=self.rejestracja)
        self.but.place(x=183, y=135)

        self.but = tk.Button(self.ramka1, text="zamknij to okno",
                             bg="#556B2F", command=self.zamknij_okno)
        self.but.place(x=250, y=135)

    def czyscioch(self):
        self.en.delete(0, END)
        self.en1.delete(0, END)
        self.en2.delete(0, END)

    def rejestracja(self):
        self.imieU = self.imie.get()

    def zamknij_okno(self):
        self.ramka1.destroy()

    def info_liczba(self):
        showinfo("Uwaga!", "Jedna z podanych liczb\n nie mieści się w zakresie 1-49")

    def info_dzien(self):
        showinfo("Uwaga!", "Liczba dni nie mieści się w zakresie 1-31")

    def info_miesiac(self):
        showinfo("Uwaga!", "Liczba miesiecy nie mieści się w zakresie 1-12")

    def info_rok(self):
        showinfo("Uwaga!", "Liczba rok nie mieści się w okreslonym zakresie")

    def info_tesame(self):
        showinfo("Uwaga!", "Jedna z liczba jest taka sama\njak pozostałe")

    def puste_pole(self):
        showinfo("Uwaga!", "Jedno pole jest puste!")

    def baza_csv(self):
        showinfo("Informacja", "Plik lotto.csv został zaimportowany!")

    def zapisz_do_bazy(self):
        self.dzienLos = self.dzien.get()
        self.miesiacLos = self.miesiac.get()
        self.rokLos = self.rok.get()
        self.numerLos = self.nLosowania.get()
        self.liczbaPi = self.liczbaJeden.get()
        self.liczbaD = self.liczbaDwa.get()
        self.liczbaT = self.liczbaTrzy.get()
        self.liczbaCz = self.liczbaCztery.get()
        self.liczbaP = self.liczbaPiec.get()
        self.liczbaSz = self.liczbaSzesc.get()

        biezaceRok = strftime("%Y")
        biezaceRok = int(biezaceRok)

        dzienLos = int(self.dzienLos)
        miesiacLos = int(self.miesiacLos)
        rokLos = int(self.rokLos)
        liczbaPi = int(self.liczbaPi)
        liczbaD = int(self.liczbaD)
        liczbaT = int(self.liczbaT)
        liczbaCz = int(self.liczbaCz)
        liczbaP = int(self.liczbaP)
        liczbaSz = int(self.liczbaSz)

        if dzienLos > 31 or dzienLos < 1:
            self.info_dzien()
        elif miesiacLos > 12 or miesiacLos < 1:
            self.info_miesiac()
        elif rokLos > biezaceRok or rokLos < 1957:
            self.info_rok()
        elif liczbaPi > 49 or liczbaPi < 1:
            self.info_liczba()
        elif liczbaD > 49 or liczbaD < 1:
            self.info_liczba()
        elif liczbaT > 49 or liczbaT < 1:
            self.info_liczba()
        elif liczbaCz > 49 or liczbaCz < 1:
            self.info_liczba()
        elif liczbaP > 49 or liczbaP < 1:
            self.info_liczba()
        elif liczbaSz > 49 or liczbaSz < 1:
            self.info_liczba()

        elif liczbaPi == liczbaD or liczbaPi == liczbaT or liczbaPi == liczbaCz or liczbaPi == liczbaP or liczbaPi == liczbaSz:
            self.info_tesame()
        elif liczbaD == liczbaT or liczbaD == liczbaCz or liczbaD == liczbaP or liczbaD == liczbaSz:
            self.info_tesame()
        elif liczbaT == liczbaCz or liczbaT == liczbaP or liczbaT == liczbaSz:
            self.info_tesame()
        elif liczbaCz == liczbaP or liczbaCz == liczbaSz:
            self.info_tesame()
        elif liczbaP == liczbaSz:
            self.info_tesame()
        else:
            conn = sqlite3.connect('baza.db')
            c = conn.cursor()
            c.execute("INSERT INTO lotto VALUES(NULL, :dzien, :miesiac, :rok, :nr_losowania, :l1, :l2, :l3, :l4, :l5, :l6)",
                      {
                          'dzien': self.dzienLos,
                          'miesiac': self.miesiacLos,
                          'rok': self.rokLos,
                          'nr_losowania': self.numerLos,
                          'l1': self.liczbaPi,
                          'l2': self.liczbaD,
                          'l3': self.liczbaT,
                          'l4': self.liczbaCz,
                          'l5': self.liczbaP,
                          'l6': self.liczbaSz
                      })
            conn.commit()
            conn.close()
            self.zamknij_okno()

    def clear_dane(self):
        self.e1.delete(0, END)
        self.e1a.delete(0, END)
        self.e1b.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete(0, END)
        self.e6.delete(0, END)
        self.e7.delete(0, END)
        self.e8.delete(0, END)

    def dodaj_liczby(self):  # dodaj swoje liczby
        self.ramka1 = Frame(root,  height=596, width=650, bg="#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side=RIGHT)

        linia1 = tk.Label(self.ramka1, text="Wstaw datę w określone pola:", font=(
            "Arial", 13), bg="#FAFAD2")
        linia1.place(x=10, y=10)

        linia1a = tk.Label(self.ramka1, text="dd",
                           font=("Arial", 13), bg="#FAFAD2")
        linia1a.place(x=240, y=10)

        linia1b = tk.Label(self.ramka1, text="mm",
                           font=("Arial", 13), bg="#FAFAD2")
        linia1b.place(x=320, y=10)

        linia1c = tk.Label(self.ramka1, text="YYYY",
                           font=("Arial", 13), bg="#FAFAD2")
        linia1c.place(x=400, y=10)

        linia2 = tk.Label(self.ramka1, text="Podaj kolejno 6 liczb:", font=(
            "Arial", 13), bg="#FAFAD2")
        linia2.place(x=10, y=50)

        self.dzienUsera = StringVar()
        self.miesiacUsera = StringVar()
        self.rokUsera = StringVar()
        self.liczba1Usera = StringVar()
        self.liczba2Usera = StringVar()
        self.liczba3Usera = StringVar()
        self.liczba4Usera = StringVar()
        self.liczba5Usera = StringVar()
        self.liczba6Usera = StringVar()

        self.ent1 = tk.Entry(
            self.ramka1, textvariable=self.dzienUsera, width=3, font=("Arial", 13))
        self.ent1.place(x=265, y=10)

        self.ent1a = tk.Entry(
            self.ramka1, textvariable=self.miesiacUsera, width=3, font=("Arial", 13))
        self.ent1a.place(x=352, y=10)

        self.ent1b = tk.Entry(
            self.ramka1, textvariable=self.rokUsera, width=3, font=("Arial", 13))
        self.ent1b.place(x=455, y=10)

        self.ent2a = tk.Entry(
            self.ramka1, textvariable=self.liczba1Usera, width=2, font=("Arial", 13))
        self.ent2a.place(x=200, y=50)

        self.ent2b = tk.Entry(
            self.ramka1, textvariable=self.liczba2Usera, width=2, font=("Arial", 13))
        self.ent2b.place(x=240, y=50)

        self.ent2c = tk.Entry(
            self.ramka1, textvariable=self.liczba3Usera, width=2, font=("Arial", 13))
        self.ent2c.place(x=280, y=50)

        self.ent2d = tk.Entry(
            self.ramka1, textvariable=self.liczba4Usera, width=2, font=("Arial", 13))
        self.ent2d.place(x=320, y=50)

        self.ent2e = tk.Entry(
            self.ramka1, textvariable=self.liczba5Usera, width=2, font=("Arial", 13))
        self.ent2e.place(x=360, y=50)

        self.ent2f = tk.Entry(
            self.ramka1, textvariable=self.liczba6Usera, width=2, font=("Arial", 13))
        self.ent2f.place(x=400, y=50)

        przycisk1 = tk.Button(self.ramka1, text="Zapisz do bazy",
                              bg="#F08080", command=self.zapisz_liczbyUsera)
        przycisk1.place(x=310, y=100)

        przycisk2 = tk.Button(self.ramka1, text="Wyczyść dane",
                              bg="#90EE90", command=self.wyczysc_dane)
        przycisk2.place(x=210, y=100)

        przycisk3 = tk.Button(self.ramka1, text=" Zamknij to okno",
                              fg="white", bg="blue", command=self.zamknij_okno)
        przycisk3.place(x=260, y=160)

    def zapisz_liczbyUsera(self):
        self.dzienU = self.dzienUsera.get()
        self.miesiacU = self.miesiacUsera.get()
        self.rokU = self.rokUsera.get()
        self.jedenU = self.liczba1Usera.get()
        self.dwaU = self.liczba2Usera.get()
        self.trzyU = self.liczba3Usera.get()
        self.czteryU = self.liczba4Usera.get()
        self.piecU = self.liczba5Usera.get()
        self.szescU = self.liczba6Usera.get()
        self.terazRokUser = strftime('%Y')
        self.terazRokUser = int(self.terazRokUser)

        if self.dzienU == "":
            self.puste_pole()
        elif self.miesiacU == "":
            self.puste_pole()
        elif self.rokU == "":
            self.puste_pole()
        elif self.jedenU == "":
            self.puste_pole()
        elif self.dwaU == "":
            self.puste_pole()
        elif self.trzyU == "":
            self.puste_pole()
        elif self.czteryU == "":
            self.puste_pole()
        elif self.piecU == "":
            self.puste_pole()
        elif self.szescU == "":
            self.puste_pole()
        else:
            self.dzienU = int(self.dzienU)
            self.miesiacU = int(self.miesiacU)
            self.rokU = int(self.rokU)
            self.jedenU = int(self.jedenU)
            self.dwaU = int(self.dwaU)
            self.trzyU = int(self.trzyU)
            self.czteryU = int(self.czteryU)
            self.piecU = int(self.piecU)
            self.szescU = int(self.szescU)

        if self.dzienU > 31 or self.dzienU < 1:
            self.info_dzien()
        elif self.miesiacU > 12 or self.miesiacU < 1:
            self.info_miesiac()
        elif self.rokU > self.terazRokUser or self.rokU < 1957:
            self.info_rok()
        elif self.jedenU == self.dwaU or self.jedenU == self.trzyU or self.jedenU == self.czteryU or self.jedenU == self.piecU or self.jedenU == self.szescU:
            self.info_tesame()
        elif self.dwaU == self.trzyU or self.dwaU == self.czteryU or self.dwaU == self.piecU or self.dwaU == self.szescU:
            self.info_tesame()
        elif self.trzyU == self.czteryU or self.trzyU == self.piecU or self.trzyU == self.szescU:
            self.info_tesame()
        elif self.czteryU == self.piecU or self.czteryU == self.szescU:
            self.info_tesame()
        elif self.piecU == self.szescU:
            self.info_tesame()
        else:
            conn = sqlite3.connect('baza.db')
            c = conn.cursor()
            c.execute("INSERT INTO liczbyUser VALUES(NULL, :dzien, :miesiac, :rok, :lu1, :lu2, :lu3, :lu4, :lu5, :lu6)",
                      {
                          'dzien': self.dzienUsera.get(),
                          'miesiac': self.miesiacUsera.get(),
                          'rok': self.rokUsera.get(),
                          'lu1': self.liczba1Usera.get(),
                          'lu2': self.liczba2Usera.get(),
                          'lu3': self.liczba3Usera.get(),
                          'lu4': self.liczba4Usera.get(),
                          'lu5': self.liczba5Usera.get(),
                          'lu6': self.liczba6Usera.get()
                      })
            conn.commit()
            conn.close()
            self.zamknij_okno()

    def wyczysc_dane(self):
        self.ent1.delete(0, END)
        self.ent1a.delete(0, END)
        self.ent1b.delete(0, END)
        self.ent2a.delete(0, END)
        self.ent2b.delete(0, END)
        self.ent2c.delete(0, END)
        self.ent2d.delete(0, END)
        self.ent2e.delete(0, END)
        self.ent2f.delete(0, END)

    def zamknij_program(self):
        root.destroy()

    def weryfikacja_liczb(self):
        self.ramka1 = Frame(root,  height=550, width=600, bg="#F0E68C")
        self.ramka1.pack(padx=5, pady=5, side=TOP)

        lab1 = tk.Label(self.ramka1, text="Wyniki ostatniego losowania:", font=(
            "Arial", 14), bg="#F0E68C")
        lab1.place(x=10, y=10)

        polozenieX = 10
        polozenieY = 40
        losowane = []
        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lotto ORDER BY id DESC LIMIT 1")
        records = c.fetchall()
        for reco in records:
            tk.Label(self.ramka1, text="data losowania: "+str(reco[2]), font=(
                "Arial", 13), bg="#F0E68C").place(x=polozenieX, y=polozenieY)
            tk.Label(self.ramka1, text="  liczby: "+str(reco[3])+", "+str(reco[4])+", "+str(reco[5])+", "+str(reco[6])+", "+str(
                reco[7])+", "+str(reco[8]), font=("Arial", 13, "bold"), bg="#F0E68C").place(x=polozenieX+250, y=polozenieY)
            losowane.append(int(reco[3]))
            losowane.append(int(reco[4]))
            losowane.append(int(reco[5]))
            losowane.append(int(reco[6]))
            losowane.append(int(reco[7]))
            losowane.append(int(reco[8]))

        conn.close()

        conn = sqlite3.connect('baza.db')
        c = conn.cursor()
        c.execute("SELECT * FROM liczbyUser")
        records = c.fetchall()

        trafienia = []
        io = 320
        ip = 80
        for re in records:
            typy_1 = int(re[4])
            typy_2 = int(re[5])
            typy_3 = int(re[6])
            typy_4 = int(re[7])
            typy_5 = int(re[8])
            typy_6 = int(re[9])
            tk.Label(self.ramka1, text="Twoje wytypowane liczby: ", font=(
                "Arial", 13), fg="green", bg="#F0E68C").place(x=polozenieX, y=polozenieY+ip)
            tk.Label(self.ramka1, text=str(re[4])+", "+str(re[5])+", "+str(re[6])+", "+str(re[7])+", "+str(re[8])+", "+str(
                re[9]), font=("Arial", 13, "bold"), fg="green", bg="#F0E68C").place(x=polozenieX+320, y=polozenieY+ip)
            ip += 30

            tk.Label(self.ramka1, text="Twoje trafienia: ", font=(
                "Arial", 13), fg="brown", bg="#F0E68C").place(x=10, y=io)
            for tt in losowane:
                if tt == typy_1 or tt == typy_2 or tt == typy_3 or tt == typy_4 or tt == typy_5 or tt == typy_6:

                    tk.Label(self.ramka1, text=tt, font=("Arial", 13),
                             fg="white", bg="green").place(x=70 + ip, y=io)
                    ip += 30
            io += 30

        conn.close()
        but = tk.Button(self.ramka1, text="zamknij to okno",
                        bg="#DC143C", command=self.zamknij_okno)
        but.place(x=270, y=510)


root = tk.Tk()
root.geometry("800x600+100+100")  # rozmiar i położenie okna
root.title("Lottomat")  # tytuł okna
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='lotto.png'))
root.resizable(False, False)  # blokowanie rozmiaru okienka

Program(root)  # uruchomienie programu

root.mainloop()
