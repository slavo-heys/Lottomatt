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
            new_item.add_command(
                label="rejestracja użytkownika", command=self.rejestracja_usera)
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

        but2 = tk.Button(self.ramka, text="Powtarzające się liczby",
                         width=18, command=self.liczby_powtorzone)
        but2.place(x=10, y=70)

        but3 = tk.Button(self.ramka, text="Analiza par",
                         width=18, command=self.analiza_par)
        but3.place(x=10, y=100)

        but4 = tk.Button(self.ramka, text="Sprawdź moje liczby",
                         width=18, command="")
        but4.place(x=10, y=130)

        but4 = tk.Button(self.ramka, text="Wyjście z programu",
                         bg="#F08080", width=18, command=self.zamknij_program)
        but4.place(x=10, y=540)

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
                    elif liczba_2 == i and liczba_3 == j:
                        pary.append([liczba_2, liczba_3])
                    elif liczba_2 == i and liczba_4 == j:
                        pary.append([liczba_2, liczba_4])
                    elif liczba_2 == i and liczba_5 == j:
                        pary.append([liczba_2, liczba_5])
                    elif liczba_2 == i and liczba_6 == j:
                        pary.append([liczba_2, liczba_6])
                    elif liczba_3 == i and liczba_4 == j:
                        pary.append([liczba_3, liczba_4])
                    elif liczba_3 == i and liczba_5 == j:
                        pary.append([liczba_3, liczba_5])
                    elif liczba_3 == i and liczba_6 == j:
                        pary.append([liczba_3, liczba_6])
                    elif liczba_4 == i and liczba_5 == j:
                        pary.append([liczba_4, liczba_5])
                    elif liczba_4 == i and liczba_6 == j:
                        pary.append([liczba_4, liczba_6])
                    elif liczba_5 == i and liczba_6 == j:
                        pary.append([liczba_5, liczba_6])

        pary.sort()

        linia1 = tk.Label(self.ramka1, text="Dwadzieścia par najczęściej występujących w losowaniach", font=(
            "Arial", 14), bg="#FAFAD2")
        linia1.place(x=30, y=20)

        lista = []
        for r in range(1, 50):
            for t in range(1, 50):
                licznik = pary.count([r, t])
                lista.append([licznik, r, t])

        lista.sort()
        r = len(lista)
        r = r-1
        t = r-20
        ypolozenie = 50
        while r > t:
            losowanie = (lista[r][0])
            liczbaPara1 = (lista[r][1])
            liczbaPara2 = (lista[r][2])
            r -= 1

            tk.Label(self.ramka1, text="Para liczb: "+str(liczbaPara1)+" - "+str(liczbaPara2) +
                     "   wystąpień: "+str(losowanie), font=("Arial", 12), bg="#FAFAD2").place(x=40, y=ypolozenie)
            ypolozenie += 25

        but = tk.Button(self.ramka1, text="zamknij to okno",
                        bg="#DC143C", command=self.zamknij_okno)
        but.place(x=400, y=500)


# definicja sprawdza powtarzające się liczby


    def liczby_powtorzone(self):
        self.ramka1 = Frame(root, height=550, width=600, bg="#E9967A")
        self.ramka1.pack(padx=5, pady=5, side=TOP)
        b = 50
        for a in range(1, 11):
            tk.Label(self.ramka1, text=" "+str(a)+" ",
                     font=("Arial", 13), bg="green").place(x=b, y=40)
            b = b+50

        b = 50
        for a in range(11, 21):
            tk.Label(self.ramka1, text=" "+str(a)+" ",
                     font=("Arial", 13), bg="green").place(x=b, y=140)
            b = b+50

        b = 50
        for a in range(21, 31):
            tk.Label(self.ramka1, text=" "+str(a)+" ",
                     font=("Arial", 13), bg="green").place(x=b, y=240)
            b = b+50

        b = 50
        for a in range(31, 41):
            tk.Label(self.ramka1, text=" "+str(a)+" ",
                     font=("Arial", 13), bg="green").place(x=b, y=340)
            b = b+50

        b = 50
        for a in range(41, 50):
            tk.Label(self.ramka1, text=" "+str(a)+" ",
                     font=("Arial", 13), bg="green").place(x=b, y=440)
            b = b+50

        l1 = 0
        l2 = 0
        l3 = 0
        l4 = 0
        l5 = 0
        l6 = 0
        l7 = 0
        l8 = 0
        l9 = 0
        l10 = 0
        l11 = 0
        l12 = 0
        l13 = 0
        l14 = 0
        l15 = 0
        l16 = 0
        l17 = 0
        l18 = 0
        l19 = 0
        l20 = 0
        l21 = 0
        l22 = 0
        l23 = 0
        l24 = 0
        l25 = 0
        l26 = 0
        l27 = 0
        l28 = 0
        l29 = 0
        l30 = 0
        l31 = 0
        l32 = 0
        l33 = 0
        l34 = 0
        l35 = 0
        l36 = 0
        l37 = 0
        l38 = 0
        l39 = 0
        l40 = 0
        l41 = 0
        l42 = 0
        l43 = 0
        l44 = 0
        l45 = 0
        l46 = 0
        l47 = 0
        l48 = 0
        l49 = 0

        lista = []

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
        l2 = lista.count(2)
        l3 = lista.count(3)
        l4 = lista.count(4)
        l5 = lista.count(5)
        l6 = lista.count(6)
        l7 = lista.count(7)
        l8 = lista.count(8)
        l9 = lista.count(9)
        l9 = lista.count(10)

        l11 = lista.count(11)
        l12 = lista.count(12)
        l13 = lista.count(13)
        l14 = lista.count(14)
        l15 = lista.count(15)
        l16 = lista.count(16)
        l17 = lista.count(17)
        l18 = lista.count(18)
        l19 = lista.count(19)
        l20 = lista.count(20)

        l21 = lista.count(21)
        l22 = lista.count(22)
        l23 = lista.count(23)
        l24 = lista.count(24)
        l25 = lista.count(25)
        l26 = lista.count(26)
        l27 = lista.count(27)
        l28 = lista.count(28)
        l29 = lista.count(29)
        l30 = lista.count(30)

        l31 = lista.count(31)
        l32 = lista.count(32)
        l33 = lista.count(33)
        l34 = lista.count(34)
        l35 = lista.count(35)
        l36 = lista.count(36)
        l37 = lista.count(37)
        l38 = lista.count(38)
        l39 = lista.count(39)
        l40 = lista.count(40)

        l41 = lista.count(41)
        l42 = lista.count(42)
        l43 = lista.count(43)
        l44 = lista.count(44)
        l45 = lista.count(45)
        l46 = lista.count(46)
        l47 = lista.count(47)
        l48 = lista.count(48)
        l49 = lista.count(49)

        self.lin1 = tk.Label(self.ramka1, text=" "+str(l1) +
                             " ", font=("Arial", 13), bg="yellow")
        self.lin1.place(x=50, y=65)

        self.lin2 = tk.Label(self.ramka1, text=" "+str(l2) +
                             " ", font=("Arial", 13), bg="yellow")
        self.lin2.place(x=100, y=65)

        self.lin3 = tk.Label(self.ramka1, text=" "+str(l3) +
                             " ", font=("Arial", 13), bg="yellow")
        self.lin3.place(x=150, y=65)

        self.lin4 = tk.Label(self.ramka1, text=" "+str(l4) +
                             " ", font=("Arial", 13), bg="yellow")
        self.lin4.place(x=200, y=65)

        self.lin5 = tk.Label(self.ramka1, text=" "+str(l5) +
                             " ", font=("Arial", 13), bg="yellow")
        self.lin5.place(x=250, y=65)

        self.lin6 = tk.Label(self.ramka1, text=" "+str(l6) +
                             " ", font=("Arial", 13), bg="yellow")
        self.lin6.place(x=300, y=65)

        self.lin7 = tk.Label(self.ramka1, text=" "+str(l7) +
                             " ", font=("Arial", 13), bg="yellow")
        self.lin7.place(x=350, y=65)

        self.lin8 = tk.Label(self.ramka1, text=" "+str(l8) +
                             " ", font=("Arial", 13), bg="yellow")
        self.lin8.place(x=400, y=65)

        self.lin9 = tk.Label(self.ramka1, text=" "+str(l9) +
                             " ", font=("Arial", 13), bg="yellow")
        self.lin9.place(x=450, y=65)

        self.lin10 = tk.Label(self.ramka1, text=" " +
                              str(l10)+" ", font=("Arial", 13), bg="yellow")
        self.lin10.place(x=500, y=65)

        self.lin11 = tk.Label(self.ramka1, text=" " +
                              str(l11)+" ", font=("Arial", 13), bg="yellow")
        self.lin11.place(x=50, y=165)

        self.lin12 = tk.Label(self.ramka1, text=" " +
                              str(l12)+" ", font=("Arial", 13), bg="yellow")
        self.lin12.place(x=100, y=165)

        self.lin13 = tk.Label(self.ramka1, text=" " +
                              str(l13)+" ", font=("Arial", 13), bg="yellow")
        self.lin13.place(x=150, y=165)

        self.lin14 = tk.Label(self.ramka1, text=" " +
                              str(l14)+" ", font=("Arial", 13), bg="yellow")
        self.lin14.place(x=200, y=165)

        self.lin15 = tk.Label(self.ramka1, text=" " +
                              str(l15)+" ", font=("Arial", 13), bg="yellow")
        self.lin15.place(x=250, y=165)

        self.lin16 = tk.Label(self.ramka1, text=" " +
                              str(l16)+" ", font=("Arial", 13), bg="yellow")
        self.lin16.place(x=300, y=165)

        self.lin17 = tk.Label(self.ramka1, text=" " +
                              str(l17)+" ", font=("Arial", 13), bg="yellow")
        self.lin17.place(x=350, y=165)

        self.lin18 = tk.Label(self.ramka1, text=" " +
                              str(l18)+" ", font=("Arial", 13), bg="yellow")
        self.lin18.place(x=400, y=165)

        self.lin19 = tk.Label(self.ramka1, text=" " +
                              str(l19)+" ", font=("Arial", 13), bg="yellow")
        self.lin19.place(x=450, y=165)

        self.lin20 = tk.Label(self.ramka1, text=" " +
                              str(l20)+" ", font=("Arial", 13), bg="yellow")
        self.lin20.place(x=500, y=165)

        self.lin21 = tk.Label(self.ramka1, text=" " +
                              str(l21)+" ", font=("Arial", 13), bg="yellow")
        self.lin21.place(x=50, y=265)

        self.lin22 = tk.Label(self.ramka1, text=" " +
                              str(l22)+" ", font=("Arial", 13), bg="yellow")
        self.lin22.place(x=100, y=265)

        self.lin23 = tk.Label(self.ramka1, text=" " +
                              str(l23)+" ", font=("Arial", 13), bg="yellow")
        self.lin23.place(x=150, y=265)

        self.lin24 = tk.Label(self.ramka1, text=" " +
                              str(l24)+" ", font=("Arial", 13), bg="yellow")
        self.lin24.place(x=200, y=265)

        self.lin25 = tk.Label(self.ramka1, text=" " +
                              str(l25)+" ", font=("Arial", 13), bg="yellow")
        self.lin25.place(x=250, y=265)

        self.lin26 = tk.Label(self.ramka1, text=" " +
                              str(l26)+" ", font=("Arial", 13), bg="yellow")
        self.lin26.place(x=300, y=265)

        self.lin27 = tk.Label(self.ramka1, text=" " +
                              str(l27)+" ", font=("Arial", 13), bg="yellow")
        self.lin27.place(x=350, y=265)

        self.lin28 = tk.Label(self.ramka1, text=" " +
                              str(l28)+" ", font=("Arial", 13), bg="yellow")
        self.lin28.place(x=400, y=265)

        self.lin29 = tk.Label(self.ramka1, text=" " +
                              str(l29)+" ", font=("Arial", 13), bg="yellow")
        self.lin29.place(x=450, y=265)

        self.lin30 = tk.Label(self.ramka1, text=" " +
                              str(l30)+" ", font=("Arial", 13), bg="yellow")
        self.lin30.place(x=500, y=265)

        self.lin31 = tk.Label(self.ramka1, text=" " +
                              str(l31)+" ", font=("Arial", 13), bg="yellow")
        self.lin31.place(x=50, y=365)

        self.lin32 = tk.Label(self.ramka1, text=" " +
                              str(l32)+" ", font=("Arial", 13), bg="yellow")
        self.lin32.place(x=100, y=365)

        self.lin33 = tk.Label(self.ramka1, text=" " +
                              str(l33)+" ", font=("Arial", 13), bg="yellow")
        self.lin33.place(x=150, y=365)

        self.lin34 = tk.Label(self.ramka1, text=" " +
                              str(l34)+" ", font=("Arial", 13), bg="yellow")
        self.lin34.place(x=200, y=365)

        self.lin35 = tk.Label(self.ramka1, text=" " +
                              str(l35)+" ", font=("Arial", 13), bg="yellow")
        self.lin35.place(x=250, y=365)

        self.lin36 = tk.Label(self.ramka1, text=" " +
                              str(l36)+" ", font=("Arial", 13), bg="yellow")
        self.lin36.place(x=300, y=365)

        self.lin37 = tk.Label(self.ramka1, text=" " +
                              str(l37)+" ", font=("Arial", 13), bg="yellow")
        self.lin37.place(x=350, y=365)

        self.lin38 = tk.Label(self.ramka1, text=" " +
                              str(l38)+" ", font=("Arial", 13), bg="yellow")
        self.lin38.place(x=400, y=365)

        self.lin39 = tk.Label(self.ramka1, text=" " +
                              str(l39)+" ", font=("Arial", 13), bg="yellow")
        self.lin39.place(x=450, y=365)

        self.lin40 = tk.Label(self.ramka1, text=" " +
                              str(l40)+" ", font=("Arial", 13), bg="yellow")
        self.lin40.place(x=500, y=365)

        self.lin41 = tk.Label(self.ramka1, text=" " +
                              str(l41)+" ", font=("Arial", 13), bg="yellow")
        self.lin41.place(x=50, y=465)

        self.lin42 = tk.Label(self.ramka1, text=" " +
                              str(l42)+" ", font=("Arial", 13), bg="yellow")
        self.lin42.place(x=100, y=465)

        self.lin43 = tk.Label(self.ramka1, text=" " +
                              str(l43)+" ", font=("Arial", 13), bg="yellow")
        self.lin43.place(x=150, y=465)

        self.lin44 = tk.Label(self.ramka1, text=" " +
                              str(l44)+" ", font=("Arial", 13), bg="yellow")
        self.lin44.place(x=200, y=465)

        self.lin45 = tk.Label(self.ramka1, text=" " +
                              str(l45)+" ", font=("Arial", 13), bg="yellow")
        self.lin45.place(x=250, y=465)

        self.lin46 = tk.Label(self.ramka1, text=" " +
                              str(l46)+" ", font=("Arial", 13), bg="yellow")
        self.lin46.place(x=300, y=465)

        self.lin47 = tk.Label(self.ramka1, text=" " +
                              str(l47)+" ", font=("Arial", 13), bg="yellow")
        self.lin47.place(x=350, y=465)

        self.lin48 = tk.Label(self.ramka1, text=" " +
                              str(l48)+" ", font=("Arial", 13), bg="yellow")
        self.lin48.place(x=400, y=465)

        self.lin49 = tk.Label(self.ramka1, text=" " +
                              str(l49)+" ", font=("Arial", 13), bg="yellow")
        self.lin49.place(x=450, y=465)

        self.przycisk = tk.Button(
            self.ramka1, text="zamknij to okno", bg="#DC143C", command=self.zamknij_okno)
        self.przycisk.place(x=250, y=510)

        conn.close()

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

    def dodaj_losowanie(self):
        self.ramka1 = Frame(root,  height=596, width=650, bg="#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side=TOP)

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
        self.e1 = tk.Entry(self.ramka1, textvariable=self.dzien,
                           font=("Arial", 13), width=3)
        self.e1.place(x=229, y=10)

        self.miesiac = StringVar()
        self.e1a = tk.Entry(self.ramka1, textvariable=self.miesiac,
                            font=("Arial", 13), width=3)
        self.e1a.place(x=316, y=10)

        self.rok = StringVar()
        self.e1b = tk.Entry(self.ramka1, textvariable=self.rok,
                            font=("Arial", 13), width=5)
        self.e1b.place(x=407, y=10)

        self.nLosowania = StringVar()
        self.e2 = tk.Entry(self.ramka1, textvariable=self.nLosowania,
                           font=("Arial", 13), width=8)
        self.e2.place(x=200, y=35)

        self.liczbaJeden = StringVar()
        self.liczbaDwa = StringVar()
        self.liczbaTrzy = StringVar()
        self.liczbaCztery = StringVar()
        self.liczbaPiec = StringVar()
        self.liczbaSzesc = StringVar()
        # liczba1
        self.e3 = tk.Entry(self.ramka1, textvariable=self.liczbaJeden,
                           font=("Arial", 13), width=2)
        self.e3.place(x=200, y=70)
        # liczba2

        self.e4 = tk.Entry(self.ramka1, textvariable=self.liczbaDwa,
                           font=("Arial", 13), width=2)
        self.e4.place(x=230, y=70)
        # liczba 3

        self.e5 = tk.Entry(self.ramka1, textvariable=self.liczbaTrzy,
                           font=("Arial", 13), width=2)
        self.e5.place(x=260, y=70)
        # liczba 4

        self.e6 = tk.Entry(self.ramka1, textvariable=self.liczbaCztery,
                           font=("Arial", 13), width=2)
        self.e6.place(x=290, y=70)
        # liczba 5

        self.e7 = tk.Entry(self.ramka1, textvariable=self.liczbaPiec,
                           font=("Arial", 13), width=2)
        self.e7.place(x=320, y=70)
        # liczba 6

        self.e8 = tk.Entry(self.ramka1, textvariable=self.liczbaSzesc,
                           font=("Arial", 13), width=2)
        self.e8.place(x=350, y=70)
        # przycisk zapisz do tabli i wyczyść dane
        przycisk1 = tk.Button(self.ramka1, text="Zapisz do bazy",
                              bg="#F08080", command=self.zapisz_do_bazy)
        przycisk1.place(x=310, y=100)

        przycisk2 = tk.Button(self.ramka1, text="Wyczyść dane",
                              bg="#90EE90", command=self.clear_dane)
        przycisk2.place(x=210, y=100)

        przycisk3 = tk.Button(self.ramka1, text=" Zamknij to okno",
                              fg="white", bg="blue", command=self.zamknij_okno)
        przycisk3.place(x=260, y=160)

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


root = tk.Tk()
root.geometry("800x600+100+100")  # rozmiar i położenie okna
root.title("Lottomat")  # tytuł okna
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='lotto.png'))
root.resizable(False, False)  # blokowanie rozmiaru okienka

Program(root)  # uruchomienie programu

root.mainloop()
