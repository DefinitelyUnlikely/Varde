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

from_date = datetime.date(2023, 3, 1)
to_date = datetime.date(2023, 3, 31)

one_year_earlier = from_date - relativedelta(years=1)

empty_cards = {'TA81218 - Telenor Prepaid TripleSIM 0kr', 'TA81258 - Telenor Prepaid TripleSIM 0kr (till 25-pack)'}
preloaded_cards = {
            'TA81228 - Telenor Prepaid TripleSIM Fast 1 månad Mini',
            'TA81259 - Telenor MBB 100 GB 1 år',
            'TA81220 - Telenor Prepaid TripleSIM Fast 1 månad',
            'TA81235 - Telenor Prepaid MBB 10Gb',
            'TA81230 - Telenor Prepaid TripleSIM Halvår',
            'TA81247 - Prepaid Startpaket HELLO',
            'TA81259 - Telenor prepaid MBB 10GB Arlo',
                    }
volvo_cards = {'TA81199 - Telenor MBB Volvo 5GB', }

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
                      r'DBQ=C:\Code\MasterMars.accdb;'
                      )


cursor = conn.cursor()

#Hämta all 
cursor.execute(f'SELECT * FROM Laddningsdata WHERE "Topup date" between #{from_date}# and #{to_date}#;')

# cursor.execute('SELECT Laddningsdata.MSISDN, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
            'FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
            'LEFT OUTER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
            f'WHERE "Topup date" between #{from_date}# and #{to_date}#'
            f'AND Activated between #{one_year_earlier}# and #{to_date}# ')     

total = 0
for i in cursor.fetchall():
       total += i.__getattribute__("Amount paid")
       
print(int(total))