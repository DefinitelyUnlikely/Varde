# En fil där vi snabbt kan testa SQL queryn för långsiktigt och tillhörande datastruktur för python.

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

cursor.execute(
    'SELECT DISTINCT Laddningsdata.MSISDN, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
    'FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
    'INNER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
    f'WHERE "Topup date" between #{from_date}# and #{to_date}#'
    f'AND Activated between #{from_date - relativedelta(years=1)}# and #{to_date}# '
    )

 
region_counter = Counter()
for i in cursor:
    # Vi hade kunnat multiplicera värdet med measure, som jag tror är antal laddningar. MEN det har inte gjorts förut, 
    # så vi väljer bort detta för att hålla datan konsekvent mot hur den togs fram tidigare. För det kan vara så att
    # Amount paid innehåller det totala värdet för antalet laddningar (dock verkar det inte så)
    region_counter[i.Region] += i.__getattribute__("Amount paid") #* i.Measure 


for reg in region_counter:
   print(reg, region_counter[reg])
   
print(f"Totalt: {sum(region_counter[reg] for reg in region_counter)}")
   

# Jag har ju ett problem, i att jag producerar ut MER värde än vi fått ut i våra mail. Det skulle kunna vara så att jag 
# också måste ta fram alla dubletter och helt enkelt räkna bort dem? Hur gör vi det? Jag får fundera.
# Det finns ett HAVING keyword, some can användas på t.ex. 

# Jag börjar få en bild av vad problemet kan vara gällande skillnaden i siffror. 1. Man har INTE räknat med measure. Det verkar udda och jag tror det 
# blir fel. Men vi släpper den. 2. JAG har en Region Jönköping som är MYCKET större än den de har i sina siffror. Jag har nog i min sifferanalys INTE
# en storecheck som har alla butiker där de "ska" vara. i.e. när ett kort aktiveras läggs det in i tabellen storecheck. Om butiken sedan byter plats
# i telenor.storecheck.se så uppdateras ju inte Storecheck tabellen. Den har ju bara sparat ned vilken butik och region kortet var i DÅ.
# Så när en butik byter region så ändras ju såklart inte tabellen i databasen. Den har kvar rätt butik, men FEL region. Jag får se om jag kan
# komma på ett sätt runt detta. 

# OM detta är sant, borde jag få mer eller mindre rätt första laddningsvärde, eller hur? För då är det bara kort som aktiverats under månaden. Har 
# inte en butik flyttas sedan kortet aktiverades ligger det i rätt region. Oddsen är små för att det är allt för mycket av det under en månad.

# En lösning kan vara att man får exportera från storecheck vald period och lägga till den csv filen i programmet. Så får programmet läsa av och uppdatera 
# storecheck. Men vi skall kolla om det är något den gör live eller om det är npgot som skall sparas. Görs det direkt så får vi ha med att man använder 
# en kopia av databasen, så att den som telenor vill ha den. Skrivs det inte över direkt utan att vi måste spara så skiter vi i att spara bara.