# En fil där vi snabbt kan testa SQL queryn för långsiktigt och tillhörande datastruktur för python. NU också där vi provar att använda 
# kopian av databasen + uppdatera den för att se vad som händer och hur det funkar.

# Hur updaterar vi på bästa sätt då? Det är många update statements om jag itererar dem. Men om vi gör det iterativt? 
# UPDATE Storecheck SET Region = "rätt region" WHERE Number = "MSISDN som vi updaterar."

import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta
import csv

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

conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\master_database_copy.accdb;'
)
cursor = conn.cursor()


cursor.execute('CREATE TABLE Updated_Store (MSISDN INTEGER, Region TEXT(100), Activated DATE, Store TEXT(255))')

with open('C:\Code\Projects\Varde\csv_files\combined-csv.csv', "r") as csvfile:
    file = csv.reader(csvfile, delimiter=",")
    next(file, None)
    for i in file:
        if i[0].isdigit():
            cursor.execute("INSERT INTO Updated_Store (MSISDN, Region, Activated, Store) VALUES (?, ?, ?, ?);", (i[0], i[3], i[2], i[5]))


cursor.execute(
    'SELECT DISTINCT Laddningsdata.MSISDN, Store, Updated_Store.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
    'FROM (Laddningsdata INNER JOIN Updated_Store ON Laddningsdata.MSISDN=Updated_Store.MSISDN) '
    'INNER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
    f'WHERE "Topup date" between #{from_date}# and #{to_date}#'
    f'AND Activated between #{from_date - relativedelta(years=1)}# and #{to_date}# '
    )

 
region_counter = Counter()
for i in cursor:
        region_counter[i.Region] += i.__getattribute__("Amount paid") #* i.Measure


for reg in region_counter:
   print(reg, region_counter[reg])
   
print(f"Totalt: {sum(region_counter[reg] for reg in region_counter)}")


# Just nu får jag väldigt lågt värde. Varför? Jo, för att jag väljer enbart att hämta csv för en månad. 
# Jag hade såklart behövt hämta en CSV som sträcker sig bakåt hela året. Jag tänkte först att vi kan 
# göra en tabell med de nya numrerna och updatera Storecheck, men då löser vi ju ändå bara 
# kort en månad bakåt. Inte längre än så. Såatteh.... bara att exporta ut året bakåt om det ska bli helt 
# korrekt. Det finns ett problem där dock. Det tar tid och servern gör en timeout. Vi får helt enkelt fundera 
# lite på detta. i.e. vi får ju ett problem om vi ska ha siffror tillbaka en viss tid liksom.

# Vi får kolla på möjligheten att kombinera csv filerna. Det betyder att man kommer behöva hämta ner 12 st csv filer för att få allting korrekt,
# Men det kanske det är värt?