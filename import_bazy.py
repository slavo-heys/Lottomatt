import sqlite3
import pandas as pd
import csv

conn = sqlite3.connect('baza.db')
c = conn.cursor()

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