# Låt oss först prova att jobba med accdb databasen. Funkar inte det, ta ut den info du behöver för att 
# göra om databasen i SQL med din struktur istället. Men det hade ju varit bäst och bekvämast för framtiden
# om vi kan använda databasen som telenor uppdaterar ändå. Då blir det inget jobb från våran sida att hålla
# SQL databasen korrekt.

import pyodbc
from os import path

# first, fix the path, so you don't have to change that all the time, I guess?


def read_db():
    conn = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\Martin\code\master_database.accdb;'
    )
    cursor = conn.cursor()
    cursor.execute('select * from Storecheck')


    for item in cursor.fetchone():
        print(item)


read_db()

