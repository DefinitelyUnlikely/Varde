# En fil där jag snabbt kan prova olika queries etc utan att hålla på i GUIn. 

import pyodbc
from collections import defaultdict, Counter
import datetime

conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\master_database.accdb;'
)
cursor = conn.cursor()

cursor.execute(
    'SELECT Number, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
    'FROM (Storecheck INNER JOIN Laddningsdata ON Storecheck.Number=Laddningsdata.MSISDN) '
    'INNER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
    'WHERE Activated between #09/30/22# and #09/30/22#'
    )


#for reg in region_map:
#    print(reg, region_map[reg])

# ladd = cursor.execute(f'SELECT * FROM Laddningsdata WHERE "Topup date" between #10/3/22# and #10/3/22#;')

# stores = cursor.execute(f"SELECT * FROM Storecheck WHERE Number IN ({', '.join(str(i.MSISDN) for i in ladd.fetchall())});")   

