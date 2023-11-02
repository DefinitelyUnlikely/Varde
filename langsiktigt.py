# En fil där vi snabbt kan testa SQL queryn för långsiktigt och tillhörande datastruktur för python.

import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

conn = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Code\Projects\Master.accdb;'
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

cursor.execute(
'SELECT Laddningsdata.MSISDN, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
'FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
'LEFT OUTER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
f'WHERE "Topup date" between #{from_date}# and #{to_date}#'
f'AND Activated between #{from_date - relativedelta(years=1)}# and #{to_date}# '
)     

store_default = defaultdict(Counter)
region_default = defaultdict(Counter)

for i in cursor:
    paid = i.__getattribute__("Amount paid")
    
    if i.Artikel in empty_cards:
        region_default[i.Region]['Tomma'] += paid
        store_default[i.Store]['Tomma'] += paid
        store_default[i.Store].setdefault('Region', i.Region)
        
    if i.Artikel in preloaded_cards:
        region_default[i.Region]['Förladdade'] += paid
        store_default[i.Store]['Förladdade'] += paid
        store_default[i.Store].setdefault('Region', i.Region)
    
region_longterm = pd.DataFrame.from_dict(region_default, orient='index')
region_longterm.index.name = "Region"
store_longterm = pd.DataFrame.from_dict(store_default, orient='index')[['Tomma', 'Förladdade', 'Region']]
store_longterm.index.name = "Butik"


# Adding gross to try and merge these

cursor.execute('SELECT Number, Store, Storecheck.Region, SIM_kort.Artikel FROM Storecheck '
               'LEFT OUTER JOIN SIM_kort ON Storecheck.Number=SIM_Kort.MSISDN '
               f'WHERE Activated between #{from_date}# and #{to_date}#')


store_default = defaultdict(Counter)
region_default = defaultdict(Counter)
for i in cursor:
    store_default[i.Store]["Totalt"] += 1
    region_default[i.Region]["Totalt"] += 1
    
    if i.Artikel in empty_cards:
        store_default[i.Store]["Tomma"] += 1
        store_default[i.Store].setdefault("Region", i.Region)
        region_default[i.Region]["Tomma"] += 1

    if i.Artikel in preloaded_cards:
        store_default[i.Store]["Förladdade"] += 1
        store_default[i.Store].setdefault("Region", i.Region)
        region_default[i.Region]["Förladdade"] += 1
        

store_gross_df = pd.DataFrame.from_dict(store_default, orient="index")[['Tomma', 'Förladdade', 'Totalt', 'Region']]
store_gross_df.index.name = "Butik"
region_gross_df = pd.DataFrame.from_dict(region_default, orient="index")[['Tomma', 'Förladdade', 'Totalt']]
region_gross_df.index.name = "Region"


merged = pd.merge(store_gross_df, store_longterm,  on="Butik", how="inner")


print(merged)