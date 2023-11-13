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
                      r'DBQ=C:\Code\Projects\dbbnov8.accdb;'
                      )


cursor = conn.cursor()

cursor.execute("SELECT * FROM SIM_Kort WHERE Artikel = NULL;")

print(cursor.fetchall())