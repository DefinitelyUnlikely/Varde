import pyodbc
import tkinter as tk
import time
import csv
from tkinter import filedialog
from tkinter import ttk
from tkcalendar import Calendar
from collections import defaultdict, Counter



class DatabaseAnalyzer():
    
    def connect_db(self):
        file_path = filedialog.askopenfilename()
        
        self.conn = pyodbc.connect(
            r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
            f'DBQ={file_path};'
            )
        self.cursor = self.conn.cursor()
        
        connLabel = tk.Label(text="Databas ansluten")
        connLabel.place(x=50, y=260)
    
    
    def quit_program(self):
        try:
            self.conn.close()
            root.quit()
        except NameError:
            root.quit()
        except AttributeError:
            root.quit()


    def import_csv(self):
        self.csv_path = filedialog.askopenfilename()
        csvLabel = tk.Label(text="CSV Importerad")
        csvLabel.place(x=50, y=290)
        

    def calculate_option(self):
        
        empty_cards = {'TA81218 - Telenor Prepaid TripleSIM 0kr', 'TA81258 - Telenor Prepaid TripleSIM 0kr (till 25-pack)'}
        preloaded_cards = {
            'TA81228 - Telenor Prepaid TripleSIM Fast 1 m�nad Mini',
            'TA81259 - Telenor MBB 100 GB 1 �r',
            'TA81220 - Telenor Prepaid TripleSIM Fast 1 m�nad',
            'TA81235 - Telenor Prepaid MBB 10Gb',
            'TA81230 - Telenor Prepaid TripleSIM Halv�r',
            'TA81247 - Prepaid Startpaket HELLO',
                    }
        volvo_cards = {'TA81199 - Telenor MBB Volvo 5GB', }
        
        
        def update_table(self):
            """
            Takes a CSV with updated region/store names from Storecheck, for the period one wants to analyze. 
            Creates a new updated table of all stores wwhich can then be joined with the current database. 
            
            """
            startLabel = tk.Label(text="Påbörjar uppdatering av regioner")
            startLabel.place(x=50, y=320)
            startLabel.update_idletasks()
            
            self.cursor.execute('CREATE TABLE Updated_Store (MSISDN INTEGER, Region TEXT(100), Activated DATE, Store TEXT(255))')

            with open(self.csv_path, "r") as csvfile:
                file = csv.reader(csvfile, delimiter=",")
                next(file, None)
                for i in file:
                    if i[0].isdigit():
                        self.cursor.execute("INSERT INTO Updated_Store (MSISDN, Region, Activated, Store) VALUES (?, ?, ?, ?);", (i[0], i[3], i[2], i[5]))
            
            startLabel['text'] = "Klar med uppdatering av regioner"            
        
        
        def longterm(self):
            """
            calculates the longterm/total value of all top ups for a given period. "longterm" is including 
            all top ups on cards less than a year old, including cards getting their first top up.
            """
            
            # If we have created an updated table for stores and regions, we use this query.
            if hasattr(self, 'csv_path'):
                self.cursor.execute(
                'SELECT Laddningsdata.MSISDN, Store, Updated_Store.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
                'FROM (Laddningsdata INNER JOIN Updated_Store ON Laddningsdata.MSISDN=Updated_Store.MSISDN) '
                'INNER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
                f'WHERE "Topup date" between #{from_cal.get_date()}# and #{to_cal.get_date()}#'
                f'AND Activated between #{earlier_string}# and #{to_cal.get_date()}# '
                )
            # Otherwise, we want to use a query where we join to the original table containing store info instead.
            else:
                self.cursor.execute(
                'SELECT Laddningsdata.MSISDN, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
                'FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
                'INNER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
                f'WHERE "Topup date" between #{from_cal.get_date()}# and #{to_cal.get_date()}#'
                f'AND Activated between #{earlier_string}# and #{to_cal.get_date()}# '
                )
            

            self.region_map = Counter()
            self.region_preloaded_map = Counter()
            self.store_map = Counter()
            self.store_preloaded_map = Counter()
            
            for i in self.cursor:
                paid = i.__getattribute__('Amount paid')
                self.region_map[i.Region] += paid
                self.store_map[i.Store] += paid
                if i.Artikel in preloaded_cards:
                    self.region_preloaded_map[i.Region] += paid
                    self.store_preloaded_map[i.Store] += paid

            doneLabel = tk.Label(text="Klar med kalkyl, programmet kan stängas")
            doneLabel.place(x=50, y=350)

 
        def first_charge(self):
            """
            Calculates the value of first charges for a given period. First charges are those on MSISDNs not top up'ed prior or 
            not top up'ed the last year.
            """
            pass
        
        
        def gross_adds(self):
            pass
            
        # If the attribute exists, a csv has been imported for use. 
        if hasattr(self, 'csv_path'):
            update_table(self)
        
        # Get relevant dates
        one_year_earlier = str(int(from_cal.get_date()[-2:]) - 1)
        earlier_string = f"{from_cal.get_date()[:-2]}{one_year_earlier}"
        
        longterm(self)

        for reg in self.region_map:
            print(reg, self.region_map[reg])
            
        print(f"Totalt: {sum(self.region_map[reg] for reg in self.region_map)}")
        
        print(f"Totalt på förladdat: {sum(self.region_preloaded_map[reg] for reg in self.region_preloaded_map)}")
        
            


db_analyzer = DatabaseAnalyzer()

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

importButton = tk.Button(calculate, text="Välj databas", command=db_analyzer.connect_db, bg="lightblue")
importButton.place(x=20, y=420)
importButton.configure(border=2, relief="raised")

csvButton = tk.Button(calculate, text="Välj csv fil", command=db_analyzer.import_csv, bg="lightblue")
csvButton.place(x=100, y=420)
csvButton.configure(border=2, relief="raised")

calculateButton = tk.Button(calculate, text="Kalkylera", command=db_analyzer.calculate_option, bg="lightblue")
calculateButton.place(x=600, y=200)

quitButton = tk.Button(text="Exit", command=db_analyzer.quit_program, fg="mint cream", bg="DarkOrange3")
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



# Väljer man butikslista så är planen liknande. Du kommer få ut en lista med mängden gross, kortsiktigt värde och långsiktigt värde 
# för varje enskild butik.

# NOTE: Vissa nummer har en extra etta i början. Den måste bort om vi skall jämföra nummer i olika tabeller.

# https://support.microsoft.com/en-us/office/examples-of-using-dates-as-criteria-in-access-queries-aea83b3b-46eb-43dd-8689-5fc961f21762
# returned_cursor.execute("SELECT * FROM Storecheck;") remember to make a SQL statement on the cursror before trying to use it.
#returned_cursor.execute("SELECT * FROM Storecheck WHERE Activated between Date() and Date()-14;") # Use Date() and Date()-number of days!!!
# returned_cursor.execute("SELECT * FROM Storecheck WHERE Activated between Date() and DateAdd('M', -6, Date())")
# returned_cursor.execute("SELECT * FROM Storecheck WHERE Activated = #11/08/2018#") specifikt datum
# Använd > eller < på istället för = om vi vill ha emellan vissa tider.
