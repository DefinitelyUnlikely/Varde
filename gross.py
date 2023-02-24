# En fil att testa SQL queries för grossen.

import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from openpyxl import load_workbook, Workbook

conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\master_feb.accdb;'
)
cursor = conn.cursor()

from_date = datetime.date(2022, 9, 1)
to_date = datetime.date(2022, 9, 30)

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
for i in cursor:
    
    if i.Artikel in empty_cards:
        store_default[i.Store]["Tomma"] += 1
        store_default[i.Store].setdefault("Region", i.Region)
        region_default[i.Region]["Tomma"] += 1

    if i.Artikel in preloaded_cards:
        store_default[i.Store]["Förladdade"] += 1
        store_default[i.Store].setdefault("Region", i.Region)
        region_default[i.Region]["Förladdade"] += 1
        

store_gross_df = pd.DataFrame.from_dict(store_default, orient="index")[['Tomma', 'Förladdade', 'Region']]
region_gross_df = pd.DataFrame.from_dict(region_default, orient="index")[['Tomma', 'Förladdade']]

print(region_gross_df)

# Hur löser jag gross? I det fallet är det väl absolut bäst att bara göra en query mot Storecheck
# Där vi tar ut alla aktiveringar inom tidsramen. Sedan delar vi upp det till regionerna.