# En fil att testa SQL queries för forsta laddning.

import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

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

cursor.execute('SELECT Storecheck.Number, Storecheck.Region, Storecheck.Store, Storecheck.Activated, SIM_kort.Artikel FROM Storecheck '
               'LEFT OUTER JOIN SIM_kort ON Storecheck.Number=SIM_kort.MSISDN '
               f'WHERE Activated between #{from_date}# and #{to_date}#')

first_dict = {}
for i in cursor:
    first_dict.update({i.Number: {"Region": i.Region, "Store": i.Store, "Activated": i.Activated, "Date": "N/A", "Amount": 0, "Article": i.Artikel}})
    
#  - datetime.timedelta(days=2)
cursor.execute('SELECT MSISDN, "Topup date", "Amount paid" FROM Laddningsdata '
               f'WHERE "Topup date" between #{from_date - datetime.timedelta(days=2)}# and #{to_date}#')


for i in cursor:
    if i.MSISDN in first_dict:
        if first_dict[i.MSISDN]["Date"] == "N/A" or first_dict[i.MSISDN]["Date"] > i.__getattribute__('Topup date'):
            first_dict[i.MSISDN]["Date"] = i.__getattribute__('Topup date')
            first_dict[i.MSISDN]["Amount"] = i.__getattribute__('Amount paid')

region_first = Counter()
store_first = defaultdict(dict)
for number in first_dict.values():
    region_first[number["Region"]] += number["Amount"]
    store_first[number["Store"]].setdefault("Region", number["Region"])
    store_first[number["Store"]].setdefault("Värde", 0)
    store_first[number["Store"]]["Värde"] += number["Amount"]
    
store_first_df = pd.DataFrame.from_dict(store_first, orient='index')
region_first_df = pd.DataFrame.from_dict(region_first, orient="index")
region_first_df.columns = ['Värde']
print(region_first_df)