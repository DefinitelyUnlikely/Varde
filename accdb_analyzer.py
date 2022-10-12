# Låt oss först prova att jobba med accdb databasen. Funkar inte det, ta ut den info du behöver för att 
# göra om databasen i SQL med din struktur istället. Men det hade ju varit bäst och bekvämast för framtiden
# om vi kan använda databasen som telenor uppdaterar ändå. Då blir det inget jobb från våran sida att hålla
# SQL databasen korrekt.
import pyodbc


# first, fix the path, so you don't have to change that all the time, I guess? ACtually, It doesn't matter. 
# The end result involves tkinter and using path finder.


def read_db():
    conn = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Code\Projects\master_database.accdb;'
    )
    cursor = conn.cursor()
    cursor.execute('select * from Storecheck')


    number, created, activated, region, chain, store = cursor.fetchone()
    
    print(int(number))
    
    cursor.execute('select MSISDN from Laddningsdata WHERE MSISDN = 708539423')
    print(cursor.fetchall())
        


read_db()

# Vissa nummer börjar med en etta, där det borde vara en nolla. Resterande har tagit bort den ledande nollan ifrån men saknar etta. 
# Jag vet inte om det innebär något speciellt, jag får undersöka det närmare. Jag får kolla så att de nummer som börjar med en etta 
# även gör detta i de andra tabellerna. Annars får jag ändra det på en nummer basis. Det vi kommer behöva fundera på här och nu är
# hur jag vill använda den struktur som finns. Storecheck tabellen används för att ta reda på vilken butik kortet tillhör, samt 
# när första laddningen gjordes. Är det förladdat tror jag det står 0 vid datumetet för aktivering. Det får vi ta en koll på. 

# NOTE: Nej, det stod inte med en etta före, så detta behöver vi ha i åtanke när vi letar efter aktiveringar.

# Fördelaktigt är att databasen verkar använda SQL queries. 

# Ska vi helt enkelt börja med att dela upp detta i vilka problem jag har? Lösa dessa ett och ett. 
# 1. Vi vill kunna kolla hur mycket gross varje butik har haft under en period. Vi vill göra samma för region. Helst alla på en gång ut i en excel fil.
# 2. Vi vill kunna kolla hur mycket värde en butik genereat under en period. Samma för region. Helst alla på en gång ut i en excel fil.
# Med de två ovannämnda sakerna kommer vi kunna göra jämförelser för tidsrammar med ett knapp tryck i slutändan. 
# 3. Vi kommer vilja kunna ta fram hur mycket första laddnnigsvärde en region haft under en period. 
# 4. vi kommer vilja kunna ta fram hur mycket långsiktigt värde en region haft under en period. 

# När dessa saker är lösta kan vi gå vidare till att skapa en GUI. Då vill jag att man skall välja databasen 
# och sedan kunna välja vad man vill göra och få det utskrivet till en excel fil, alterantivt i något annat format som 
# är enkelt att använda.
