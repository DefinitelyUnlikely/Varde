import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from openpyxl import load_workbook, Workbook


# Vad behöver jag göra? 
# Koppla upp till databasen
# välja SIM_Kort tabellen. 
# Gå över den tabellen, om artikel saknas, lägg till nummer i en lista?


empty_cards = {'TA81218 - Telenor Prepaid TripleSIM 0kr', 'TA81258 - Telenor Prepaid TripleSIM 0kr (till 25-pack)'}
preloaded_cards = {
            'TA81228 - Telenor Prepaid TripleSIM Fast 1 månad Mini',
            'TA81259 - Telenor MBB 100 GB 1 år',
            'TA81220 - Telenor Prepaid TripleSIM Fast 1 månad',
            'TA81235 - Telenor Prepaid MBB 10Gb',
            'TA81230 - Telenor Prepaid TripleSIM Halvår',
            'TA81247 - Prepaid Startpaket HELLO',
                    }
volvo_cards = {'TA81199 - Telenor MBB Volvo 5GB', }

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
                      r'DBQ=C:\Code\Projects\Master.accdb;'
                      )


cursor = conn.cursor()

cursor.execute("SELECT * FROM SIM_Kort")

x = 0
y = 0
z = 0
for i in cursor:
    if i.Artikel in empty_cards:
        x += 1
    if i.Artikel in preloaded_cards:
        y += 1
    if i.Artikel in volvo_cards:
        z += 1
        
print(x, y, z)
print(x + y + z)       
# totalt 1019890 när man kör alla kort

# totalt 550099 när man kör alla tomma
# totalt 457172 när man kör alla pre
# totalt 12619 när man kör alla volvo
# som har summan 1019890. Det betyder att inga kort saknar artikel.
