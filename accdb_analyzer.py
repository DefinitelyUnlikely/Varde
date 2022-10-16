# Låt oss först prova att jobba med accdb databasen. Funkar inte det, ta ut den info du behöver för att 
# göra om databasen i SQL med din struktur istället. Men det hade ju varit bäst och bekvämast för framtiden
# om vi kan använda databasen som telenor uppdaterar ändå. Då blir det inget jobb från våran sida att hålla
# SQL databasen korrekt.
import pyodbc
import tkinter as tk
from tkinter import filedialog
from tkcalendar import Calendar

# first, fix the path, so you don't have to change that all the time, I guess? ACtually, It doesn't matter. 
# The end result involves tkinter and using path finder.


def connect_db():
    global conn, cursor
    file_path = filedialog.askopenfilename()
    conn = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    f'DBQ={file_path};'
    )
    cursor = conn.cursor()
    

def calculate_option():
    if var.get() == 1:
        cursor.execute(f"SELECT * FROM Storecheck WHERE Activated between #{from_cal.get_date()}# and #{to_cal.get_date()}#;")
        for i in cursor.fetchall():
            print(i)
    if var.get() == 2:
        print("Currently Testing")


def quit_program():
    try:
        conn.close()
        root.quit()
    except NameError:
        root.quit()



root = tk.Tk()


root.title("Badabing, Badaboom")
root.geometry("1000x500+500+500")
root.configure(bg='lightblue')

var = tk.IntVar()
radio1 = tk.Radiobutton(root, text="Regionslista", variable=var, value=1)
radio2 = tk.Radiobutton(root, text="Butikslista", variable=var, value=2)
radio1.place(x=600, y=50)
radio2.place(x=600, y=70)
radioLabel = tk.Label(root, text="Välj typ av output").place(x=600, y=20)

importButton = tk.Button(text="Välj databas", command=connect_db)
importButton.place(x=20, y=450)
importButton.configure(border=2, relief="raised")

calculateButton = tk.Button(text="Kalkylera", command=calculate_option)
calculateButton.place(x=600, y=200)

quitButton = tk.Button(text="Exit", command=quit_program, fg="mint cream", bg="gray25")
quitButton.place(y=450, x=960)
quitButton.configure(border=2, relief="raised")

from_cal_label = tk.Label(root, text="Från Datum").place(x=50, y=20)
from_cal = Calendar(root)
from_cal.place(x=50, y=50)

to_cal_label = tk.Label(root, text="Till Datum").place(x=320, y=20)
to_cal = Calendar(root)
to_cal.place(x=320, y=50)


root.mainloop()  


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