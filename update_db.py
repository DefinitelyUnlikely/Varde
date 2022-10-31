# En fil där vi snabbt kan testa SQL queryn för långsiktigt och tillhörande datastruktur för python. NU också där vi provar att använda 
# kopian av databasen + uppdatera den för att se vad som händer och hur det funkar.

# Hur updaterar vi på bästa sätt då? Det är många update statements om jag itererar dem. Men om vi gör det iterativt? 
# UPDATE Storecheck SET Region = "rätt region" WHERE Number = "MSISDN som vi updaterar."

import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta
import csv


conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\master_database_copy.accdb;'
)
cursor = conn.cursor()

cursor.execute('CREATE TABLE Test (MSISDN INTEGER, Region TEXT(100))')

with open('C:\Code\Projects\Varde\csv_files\combined-csv.csv', "r") as csvfile:
    file = csv.reader(csvfile, delimiter=",")
    next(file, None)
    for i in file:
        if i[0].isdigit():
            cursor.execute("INSERT INTO Test (MSISDN, Region) VALUES (?, ?);", (i[0], i[3]))

cursor.execute("SELECT * FROM Test")
for i in cursor:
    print(i)

