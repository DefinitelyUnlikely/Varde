# En fil att testa SQL queries för grossen.

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


cursor.execute('SELECT * FROM Storecheck '
               f'WHERE Activated between #{from_date}# and #{to_date}#')


gross_map = Counter()
for i in cursor:
    gross_map[i.Region] += 1
    
for reg, val in gross_map.items():
    print(reg, val)


# Hur löser jag gross? I det fallet är det väl absolut bäst att bara göra en query mot Storecheck
# Där vi tar ut alla aktiveringar inom tidsramen. Sedan delar vi upp det till regionerna.