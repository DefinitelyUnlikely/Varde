# Låt oss först prova att jobba med accdb databasen. Funkar inte det, ta ut den info du behöver för att 
# göra om databasen i SQL med din struktur istället. Men det hade ju varit bäst och bekvämast för framtiden
# om vi kan använda databasen som telenor uppdaterar ändå. Då blir det inget jobb från våran sida att hålla
# SQL databasen korrekt.
import pyodbc
import tkinter as tk
import datetime
from tkcalendar import Calendar

# first, fix the path, so you don't have to change that all the time, I guess? ACtually, It doesn't matter. 
# The end result involves tkinter and using path finder.


def get_dates():
    print(f"Selected Dates are From {from_cal.get_date()} To {to_cal.get_date()}")

def connect_db():
    conn = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Code\Projects\master_database.accdb;'
    )
    cursor = conn.cursor()

    return conn, cursor


def gross(gross_cursor):
    pass


def varde():
    returned_cursor.execute(f"SELECT * FROM Storecheck WHERE Activated between #{from_cal.get_date()}# and #{to_cal.get_date()}# AND Region = '';")
    for i in returned_cursor.fetchall():
        print(i)


    
    
returned_conn, returned_cursor = connect_db()


root = tk.Tk()

root.title("Badabing, Badaboom")
root.geometry("1380x640+640+300")
root.configure(bg='lightblue')

from_cal_label = tk.Label(root, text="Från Datum").grid(row=0, column=0, padx=20)
from_cal = Calendar()
from_cal.grid(row=1, column=0, pady=20)

to__cal_label = tk.Label(root, text="Till Datum").grid(row=0, column=1, padx=20)
to_cal = Calendar()
to_cal.grid(row=1, column=1, padx=20)

managerLabel = tk.Label(text="Region")
managerLabel.grid(row=0, column=3, sticky="nsew", padx=20)
managerLabel.configure(bg="gray16", fg="mint cream")

managerList = tk.Listbox(root, fg="mint cream", bg="gray25")
managerList.grid(row=1, column=3, padx=20)
managerList.configure(relief="sunken")

managerScroll = tk.Scrollbar(root, orient=tk.VERTICAL, command=managerList.yview)
managerScroll.grid(row=1, column=3, sticky="nse")
managerList["yscrollcommand"] = managerScroll.set

tk.Button(text="Välj Datum", command=get_dates).grid(row=2, column=1)

tk.Button(text="Kalkylera Värde", command=varde).grid(row=4, column=4,  sticky="s")

root.mainloop()  

returned_conn.close()

# https://support.microsoft.com/en-us/office/examples-of-using-dates-as-criteria-in-access-queries-aea83b3b-46eb-43dd-8689-5fc961f21762
# returned_cursor.execute("SELECT * FROM Storecheck;") remember to make a SQL statement on the cursror before trying to use it.
#returned_cursor.execute("SELECT * FROM Storecheck WHERE Activated between Date() and Date()-14;") # Use Date() and Date()-number of days!!!
# returned_cursor.execute("SELECT * FROM Storecheck WHERE Activated between Date() and DateAdd('M', -6, Date())")
# returned_cursor.execute("SELECT * FROM Storecheck WHERE Activated = #11/08/2018#") specifikt datum
# Använd > eller < på istället för = om vi vill ha emellan vissa tider.


# Men vi måste ändå lista ut även hur man skriver in datum. Jag vill kunna ge dem en kalender att välja ur. 



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


# Hur löser vi våra subproblem? Via tabellen storecheck kan jag ta reda på när ett kort aktiverades och vilken butik kortet tillhör.
# Via Laddningsvärde kan jag ta reda på topup.

# Ska vi iterera över storecheck och kolla varje kort? Ska vi kolla varke kort och gå in i storecheck? 
# Vilken lösning är bäst?

# Vi skall nog börja i änden att man väljer datum. Därefter gör vi en query på datum i både storecheck och laddningsvärde och häntar till 
# vår backend? Eller vill vi göra det med SQL queries?