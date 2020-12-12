from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from time import strftime
import random
from PIL import ImageTk, Image
import time
from tkinter.messagebox import showinfo

# Tworzenie bazy , jeśli nie istnieje
conn = sqlite3.connect('baza.db')
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS lotto(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dzien text NOT NULL,
        miesiac text NOT NULL,
        rok text NOT NULL,
        nr_losowania text NOT NULL,
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
        self.ramka1 = Frame(root,  height=200, width=650, bg="#FAFAD2")
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
            self.info_miesiac
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
                          'l1': self.liczbaP,
                          'l2': self.liczbaD,
                          'l3': self.liczbaT,
                          'l4': self.liczbaCz,
                          'l5': self.liczbaP,
                          'l6': self.liczbaSz
                      })
            conn.commit()
            conn.close()
            self.zamknij_okno()
            print("zapisano")

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
