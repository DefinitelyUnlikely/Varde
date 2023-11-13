# En fil att testa SQL queries för grossen.

import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from openpyxl import load_workbook, Workbook

conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\Master.accdb;'
)
cursor = conn.cursor()

from_date = datetime.date(2023, 9, 1)
to_date = datetime.date(2023, 9, 30)

empty_cards = {'TA81218 - Telenor Prepaid TripleSIM 0kr', 'TA81258 - Telenor Prepaid TripleSIM 0kr (till 25-pack)'}
preloaded_cards = {'TA81228 - Telenor Prepaid TripleSIM Fast 1 månad Mini',
                   'TA81259 - Telenor MBB 100 GB 1 år',
                   'TA81220 - Telenor Prepaid TripleSIM Fast 1 månad',
                   'TA81235 - Telenor Prepaid MBB 10Gb',
                   'TA81230 - Telenor Prepaid TripleSIM Halvår',
                   'TA81247 - Prepaid Startpaket HELLO',
                   }
volvo_cards = {'TA81199 - Telenor MBB Volvo 5GB', }


cursor.execute('SELECT Number, Store, Storecheck.Region, SIM_kort.Artikel FROM Storecheck '
               'LEFT OUTER JOIN SIM_kort ON Storecheck.Number=SIM_Kort.MSISDN '
               f'WHERE Activated between #{from_date}# and #{to_date}#')


store_default = defaultdict(Counter)
region_default = defaultdict(Counter)
missing = 0
for i in cursor:
    store_default[i.Store]["Totalt"] += 1
    region_default[i.Region]["Totalt"] += 1
    
    if i.Artikel in empty_cards:
        store_default[i.Store]["Tomma"] += 1
        store_default[i.Store].setdefault("Region", i.Region)
        region_default[i.Region]["Tomma"] += 1

    elif i.Artikel in preloaded_cards:
        store_default[i.Store]["Förladdade"] += 1
        store_default[i.Store].setdefault("Region", i.Region)
        region_default[i.Region]["Förladdade"] += 1
        
    
    elif i.Artikel not in volvo_cards:
        print(i)
        missing += 1

print(missing)
store_gross_df = pd.DataFrame.from_dict(store_default, orient="index")[['Tomma', 'Förladdade', 'Totalt', 'Region']]
region_gross_df = pd.DataFrame.from_dict(region_default, orient="index")[['Tomma', 'Förladdade', 'Totalt']]


