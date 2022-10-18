# En fil där jag snabbt kan prova olika queries etc utan att hålla på i GUIn. 

import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta

conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\master_database.accdb;'
)
cursor = conn.cursor()

from_date = datetime.date(2022, 9, 30)
to_date = datetime.date(2022, 9, 30)




# För att hämta långsiktigt värde. Vi tar alla laddnignar inom en period.
# Vi JOINar Storecheck på dessa nummer så att vi kan koppla till butik och region, samt kolla aktiveringsdatum.
# Vi JOINar sedan även SIM_kort, för att kunna kolla vilken typ av kort det gäller. Så att vi senare kan dela 
# in all data i förladdat/oladdat. Men det är för framtiden. Vi oroar oss först om att fixa värdet, punkt.

cursor.execute(
    'SELECT Laddningsdata.MSISDN, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
    'FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
    'INNER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
    f'WHERE "Topup date" between #{from_date}# and #{to_date}#'
    f'AND Activated between #{to_date - relativedelta(years=1)}# and #{to_date}#'
    )
 
for i in cursor.fetchall():
    print(i)



#for reg in region_map:
#    print(reg, region_map[reg])

# ladd = cursor.execute(f'SELECT * FROM Laddningsdata WHERE "Topup date" between #10/3/22# and #10/3/22#;')

# stores = cursor.execute(f"SELECT * FROM Storecheck WHERE Number IN ({', '.join(str(i.MSISDN) for i in ladd.fetchall())});")   

