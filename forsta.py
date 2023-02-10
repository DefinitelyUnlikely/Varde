# En fil att testa SQL queries för forsta laddning.

import pyodbc
from collections import defaultdict, Counter
import datetime
from dateutil.relativedelta import relativedelta

conn = pyodbc.connect(
r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
r'DBQ=C:\Code\Projects\master_update.accdb;'
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

# Ta fram alla gross för perioden.
cursor.execute('SELECT * FROM Storecheck '
               f'WHERE Activated between #{from_date}# and #{to_date}#')


# skapa dictionary
first_dict = {}
for i in cursor:
    first_dict.update({i[0]: {"Region": i[3], "Store": i[5], "Activated": i[2], "Date": "N/A", "Amount": 0}})
    
#  - datetime.timedelta(days=2)
cursor.execute('SELECT MSISDN, "Topup date", "Amount paid" FROM Laddningsdata '
               f'WHERE "Topup date" between #{from_date}# and #{to_date}#')


for i in cursor:
    if i[0] in first_dict:
        if first_dict[i[0]]["Date"] == "N/A" or first_dict[i[0]]["Date"] > i[1]:
            first_dict[i[0]]["Date"] = i[1]
            first_dict[i[0]]["Amount"] = i[2]

region_first = Counter()
store_first = Counter()
for i in first_dict.values():
    region_first[i["Region"]] += i["Amount"]
    store_first[i["Store"]] += i["Amount"]
    
total = 0
for i in region_first:
    print(i, region_first[i])
    total += region_first[i]
    
print(total)

# Alright. Första laddning. En topup har ett topup datum. Det är kopplat till ett nummer. Det numret hittar jag också i Storecheck. 
# I Storecheck kommer numret ha ett Aktiverat datum. Om topupen skedde tidigare eller samma dag som aktiveringen, så är det första laddningen.
# Är topupen senare än aktiveringen är det inte första laddningen på kortet.


# Just nu tänker jag så här: Vi tar fram alla gross för perioden. Vi tar fram alla laddningar för perioden och ett år tillbaka. 
# Vi gör en dictionary som ser ut typ såhär: {number: {date: , topup: , activated: ,}}. och fyller den med relevant info. 
# Sedan gör vi så att vi går igenom laddningsdatan och fyller på med datum och värde. Ett äldre datum ersätter ett yngre datum. 

# Vi behöver väl fakitskt också ha med region och butik, så att vi kan koppla vart första laddningen ska till.

# Problem med upplägget? Jag är osäker på vad första laddning skall innebära. När vi gör såhär får vi ENBART första laddning 
# på de gross som skedde under perioden. Aktiverades inte kortet i Storecheck under perioden så kommer det alltså inte vara med. 
# Så ett kort som såldes för länge sedan och "återaktiveras" kommer inte räknas. MEN är det ett problem egentligen? Ett kort som 
# aktiverades i maj 2021 och har laddning till juni 2021 kommer i juni 2022 att churnas från systemet. För att det skall bli en
# återaktivering måste personen i fråga ringa in och få det upplåst och återkativerat manuellt. Det kan inte vara många kort det 
# handlar om. Så är det relevant? Nej, antagligen inte. Det är väl ändå så att det vi egentligen vill veta är hur mycket värde det
# var på de faktiskt sålda och aktiverade korten för perioden. Inte kort som kommer tillbaka. 

# Om vi tänker så, då kanske vi inte behöver ta fram laddningar från (långt innan) perioden? Bara några dagar innan för att fånga upp 
# att det laggar lite mellan topup och aktivering. Så kollar vi igenom den datan efter rätt laddning. Det tror jag blir bra.