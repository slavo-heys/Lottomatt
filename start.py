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
    def __init__(self,master):
        

        



        def MenuRozwijane(self):
            menu = Menu(root)

            new_item = Menu(menu)
            menu.add_cascade(label="Program", menu=new_item)
            new_item.add_command(label="rejestracja użytkownika",command="")
            new_item.add_separator()
            new_item.add_command(label="wyjście z programu", command="")
            
            new_obsl = Menu(menu)
            menu.add_cascade(label="Help", menu=new_obsl)
            new_obsl.add_command(label="pomoc", command="")
            
            root.config(menu=menu)

        

        MenuRozwijane(self)

        self.ramka = Frame(root, height = 596, width= 160, bg = "#FAEBD7")
        self.ramka.pack(padx=5, pady=5, side=LEFT)
        

        linia = tk.Label(self.ramka, text ="moja ramka", justify=LEFT)
        linia.place(x=500, y=10)

        but0=tk.Button(self.ramka, text="Dodaj losowanie", width=18, command = self.dodaj_losowanie)
        but0.place(x=10,y=10)

        but1=tk.Button(self.ramka, text="Dodaj swoje liczby ", width=18, command = self.dodaj_liczby)
        but1.place(x=10,y=40)

        but2=tk.Button(self.ramka, text="Powtarzające się liczby", width=18, command = "")
        but2.place(x=10,y=70)

        but3=tk.Button(self.ramka, text="Analiza par", width=18, command = "")
        but3.place(x=10,y=100)

        but4=tk.Button(self.ramka, text="Sprawdź moje liczby", width=18, command = "")
        but4.place(x=10,y=130)

        but4=tk.Button(self.ramka, text="Wyjście z programu", bg = "#F08080",width=18, command = self.zamknij_program)
        but4.place(x=10,y=180)

        

    def dodaj_losowanie(self):
        self.ramka1 = Frame(root,  height = 596, width= 650, bg = "#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side = RIGHT)

    def dodaj_liczby(self):
        self.ramka1 = Frame(root,  height = 596, width= 650, bg = "#FAFAD2")
        self.ramka1.pack(padx=5, pady=5, side = RIGHT)
    
    def zamknij_program(self):
        root.destroy()
           

root = tk.Tk()
root.geometry("800x600+100+100")  # rozmiar i położenie okna
root.title("Lottomat")  # tytuł okna
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='lotto.png'))
root.resizable(False, False)  # blokowanie rozmiaru okienka

Program(root)  # uruchomienie programu

root.mainloop()