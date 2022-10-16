# En fil där jag snabbt kan prova olika queries etc utan att hålla på i GUIn. 

import pyodbc

conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\master_database.accdb;'
)
cursor = conn.cursor()


cursor.execute('SELECT * FROM Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number WHERE "Topup date" between #10/3/22# and #10/3/22#;')

for i in cursor.fetchall():
    print(i.MSISDN, i.Activated, i.Store)

# ladd = cursor.execute(f'SELECT * FROM Laddningsdata WHERE "Topup date" between #10/3/22# and #10/3/22#;')

# stores = cursor.execute(f"SELECT * FROM Storecheck WHERE Number IN ({', '.join(str(i.MSISDN) for i in ladd.fetchall())});")   

