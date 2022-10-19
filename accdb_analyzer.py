import pyodbc
import tkinter as tk
import datetime
from tkinter import filedialog
from tkinter import ttk
from tkcalendar import Calendar
from collections import defaultdict, Counter


def connect_db():
    global conn, cursor
    file_path = filedialog.askopenfilename()
    conn = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    f'DBQ={file_path};'
    )
    cursor = conn.cursor()
    print("connected")
    

def calculate_option():
    
    empty_cards = {'TA81218 - Telenor Prepaid TripleSIM 0kr', 'TA81258 - Telenor Prepaid TripleSIM 0kr (till 25-pack)'}
    preloaded_cards = {'TA81228 - Telenor Prepaid TripleSIM Fast 1 m�nad Mini',
                   'TA81259 - Telenor MBB 100 GB 1 �r',
                   'TA81220 - Telenor Prepaid TripleSIM Fast 1 m�nad',
                   'TA81235 - Telenor Prepaid MBB 10Gb',
                   'TA81230 - Telenor Prepaid TripleSIM Halv�r',
                   'TA81247 - Prepaid Startpaket HELLO',
                   }
    volvo_cards = {'TA81199 - Telenor MBB Volvo 5GB', }
    
    if var.get() == 1:
        print("Currently Testing Regionlista")
        
        # Då .get_date() är ett string objekt blev det svårt att använda timedelta etc. Synd, det är nog en bättre 
        # lösning egentligen. Men detta verkar funka. Vi får hålla lite koll på detta och edge cases (typ skottår)
        one_year_earlier = str(int(to_cal.get_date()[-2:]) - 1)
        earlier_string = f"{to_cal.get_date()[:-2]}{one_year_earlier}"
        
        cursor.execute(
            'SELECT Laddningsdata.MSISDN, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
            'FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
            'INNER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
            f'WHERE "Topup date" between #{from_cal.get_date()}# and #{to_cal.get_date()}#'
            f'AND Activated between #{earlier_string}# and #{to_cal.get_date()}# '
            )
        
        for i in cursor.fetchone():
            print(i)

        #region_map = Counter()
        #store_map = Counter()
        #for i in cursor.fetchall():
        #    region_map[i.Region] += i.Measure * i.__getattribute__('Amount paid')
        #    store_map[i.Store] += i.Measure * i.__getattribute__('Amount paid')


        #for reg in region_map:
        #    print(reg, region_map[reg])

    if var.get() == 2:
        print("Currently Testing Butikslista")


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

tabControl = ttk.Notebook(root)

calculate = ttk.Frame(tabControl)
instructions = ttk.Frame(tabControl)
tabControl.add(calculate, text='Kalkylator')
tabControl.add(instructions, text='Instruktioner')
tabControl.place(x=0, y=0, width=1000, height=500 )

var = tk.IntVar()
radio1 = tk.Radiobutton(calculate, text="Regionslista", variable=var, value=1)
radio2 = tk.Radiobutton(calculate, text="Butikslista", variable=var, value=2)
radio1.place(x=600, y=50)
radio2.place(x=600, y=70)
radioLabel = tk.Label(calculate, text="Välj typ av output").place(x=600, y=20)

importButton = tk.Button(calculate, text="Välj databas", command=connect_db)
importButton.place(x=20, y=420)
importButton.configure(border=2, relief="raised")

calculateButton = tk.Button(calculate, text="Kalkylera", command=calculate_option)
calculateButton.place(x=600, y=200)

quitButton = tk.Button(text="Exit", command=quit_program, fg="mint cream", bg="DarkOrange3")
quitButton.place(y=450, x=960)
quitButton.configure(border=2, relief="raised")

from_cal_label = tk.Label(calculate, text="Från Datum").place(x=50, y=20)
from_cal = Calendar(calculate)
from_cal.place(x=50, y=50)

to_cal_label = tk.Label(calculate, text="Till Datum").place(x=320, y=20)
to_cal = Calendar(calculate)
to_cal.place(x=320, y=50)


instructionsText = """
1. Om programmet inte fungerar, behöver man mest troligt installera
en driver. För Windows: https://www.microsoft.com/en-US/download/details.aspx?id=13255
Om man använder UNIX (MacOS/Linux) 
"""
instructionsLabel = tk.Label(instructions, bg='gray20', fg='white', text=instructionsText)
instructionsLabel.place(x=50, y=50)


root.mainloop()  


# Alright. Nuvarande plan: Man väljer databas, från vilka datum man vill ha information och om man vill ha region eller butikslista. 
# regionslistan skall ta fram mängden gross, kortsiktigt värde + långsiktigt värde för varje region. Sedan exportera dettta till en excel fil?
# Eller vill vi printa det direkt i programmet på något sätt? 

# Väljer man butikslista så är planen liknande. Du kommer få ut en lista med mängden gross, kortsiktigt värde och långsiktigt värde 
# för varje enskild butik.

# NOTE: Vissa nummer har en extra etta i början. Den måste bort om vi skall jämföra nummer i olika tabeller.

# https://support.microsoft.com/en-us/office/examples-of-using-dates-as-criteria-in-access-queries-aea83b3b-46eb-43dd-8689-5fc961f21762
# returned_cursor.execute("SELECT * FROM Storecheck;") remember to make a SQL statement on the cursror before trying to use it.
#returned_cursor.execute("SELECT * FROM Storecheck WHERE Activated between Date() and Date()-14;") # Use Date() and Date()-number of days!!!
# returned_cursor.execute("SELECT * FROM Storecheck WHERE Activated between Date() and DateAdd('M', -6, Date())")
# returned_cursor.execute("SELECT * FROM Storecheck WHERE Activated = #11/08/2018#") specifikt datum
# Använd > eller < på istället för = om vi vill ha emellan vissa tider.
