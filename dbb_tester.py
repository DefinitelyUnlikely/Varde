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

# För att hämta långsiktigt värde. Vi tar alla laddnignar inom en period.
# Vi JOINar Storecheck på dessa nummer så att vi kan koppla till butik och region, samt kolla aktiveringsdatum.
# Vi JOINar sedan även SIM_kort, för att kunna kolla vilken typ av kort det gäller. Så att vi senare kan dela 
# in all data i förladdat/oladdat. Men det är för framtiden. Vi oroar oss först om att fixa värdet, punkt.

# Jag får ett annat värde än det som har blivit utskickat till mig när det gäller budget. Jag hittar alltså fler 
# laddningar än vad som hittats förut. Det tycker jag är lite konstigt. Provar jag att använda SIM_kort.Region 
# så går istället långsiktigt värde ner och blir MINDRE än det man skickat ut. 

# MEN! Min bör vara den mest korrekta? Jag tar alla laddningar som gjorts under en månad. Jag kopplar 
# region och butik etc till numret. Jag itererar över alla laddningar och lägger in dem på 
# regionen de hör till. SÅ, det är antagligen så att man missat något förut? Tar jag bort 
# measure som en faktor (alltså, antalet laddningar, antar jag) så går värdet ner markant. 
# Även detta under vad som skickades ut till mig för min region. Jag vet alltså inte riktigt 
# vad man har missat? Jag får se om jag kan få en kopia på ett gammalt excel som Viktor gjort 
# för detta.

cursor.execute(
    'SELECT Laddningsdata.MSISDN, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
    'FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
    'INNER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
    f'WHERE "Topup date" between #{from_date}# and #{to_date}#'
    f'AND Activated between #{to_date - relativedelta(years=1)}# and #{to_date}#'
    )
 


# Vi får typ använda setdefault på en vanlig dict, och göra defaulten för en region till en dict med allt vi behöver.
region_counter = Counter()
for i in cursor:
        region_counter[i.Region] += i.__getattribute__("Amount paid") * i.Measure


for reg in region_counter:
   print(reg, region_counter[reg])
   

# ladd = cursor.execute(f'SELECT * FROM Laddningsdata WHERE "Topup date" between #10/3/22# and #10/3/22#;')

# stores = cursor.execute(f"SELECT * FROM Storecheck WHERE Number IN ({', '.join(str(i.MSISDN) for i in ladd.fetchall())});")   

