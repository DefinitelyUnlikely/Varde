# En fil att testa SQL queries för forsta laddning.

import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta

conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\master_database.accdb;'
)
cursor = conn.cursor()

from_date = datetime.date(2022, 9, 1)
to_date = datetime.date(2022, 9, 30)

empty_cards = {'TA81218 - Telenor Prepaid TripleSIM 0kr', 'TA81258 - Telenor Prepaid TripleSIM 0kr (till 25-pack)'}
preloaded_cards = {'TA81228 - Telenor Prepaid TripleSIM Fast 1 m�nad Mini',
                   'TA81259 - Telenor MBB 100 GB 1 �r',
                   'TA81220 - Telenor Prepaid TripleSIM Fast 1 m�nad',
                   'TA81235 - Telenor Prepaid MBB 10Gb',
                   'TA81230 - Telenor Prepaid TripleSIM Halv�r',
                   'TA81247 - Prepaid Startpaket HELLO',
                   }
volvo_cards = {'TA81199 - Telenor MBB Volvo 5GB', }

cursor.execute('')

# Alright. Första laddning. En topup har ett topup datum. Det är kopplat till ett nummer. Det numret hittar jag också i Storecheck. 
# I Storecheck kommer numret ha ett Aktiverat datum. Om topupen skedde tidigare eller samma dag som aktiveringen, så är det första laddningen.
# Är topupen senare än aktiveringen är det inte första laddningen på kortet.