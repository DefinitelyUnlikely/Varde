# En fil där jag snabbt kan prova olika queries etc utan att hålla på i GUIn. 

import pyodbc
from collections import defaultdict, Counter

conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\master_database.accdb;'
)
cursor = conn.cursor()

cursor.execute('SELECT * FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
               'INNER JOIN SIM_kort ON Storecheck.number=SIM_Kort.MSISDN '
               'WHERE "Topup date" between #09/1/22# and #09/30/22#;')

# i[1] = i.Topup date, i[3] = Amount paid

region_map = Counter()
store_map = Counter()
for i in cursor.fetchall():
    # print(i.MSISDN, i[1], i.Activated, i.Store, i.Region, (i.Measure * i[3]))
    region_map[i.Region] += i.Measure * i[3]
    store_map[i.Store] += i.Measure * i[3]
    # Ska jag inte ha med measure? Jag antog att det var antalet laddningar. Utan den blir värdet mycket närmare 
    # det jag fick i budget mailen.


for reg in region_map:
    print(reg, region_map[reg])

# ladd = cursor.execute(f'SELECT * FROM Laddningsdata WHERE "Topup date" between #10/3/22# and #10/3/22#;')

# stores = cursor.execute(f"SELECT * FROM Storecheck WHERE Number IN ({', '.join(str(i.MSISDN) for i in ladd.fetchall())});")   

