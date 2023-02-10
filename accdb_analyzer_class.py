import pyodbc
import tkinter as tk
import datetime
from dateutil.relativedelta import relativedelta
import csv
from tkinter import filedialog
from tkinter import ttk
from tkcalendar import Calendar
from collections import defaultdict, Counter
import pandas as pd



class DatabaseAnalyzer():
    
    
    def __init__(self):
        
    
        self.empty_cards = {'TA81218 - Telenor Prepaid TripleSIM 0kr', 'TA81258 - Telenor Prepaid TripleSIM 0kr (till 25-pack)'}
        self.preloaded_cards = {
            'TA81228 - Telenor Prepaid TripleSIM Fast 1 m�nad Mini',
            'TA81259 - Telenor MBB 100 GB 1 �r',
            'TA81220 - Telenor Prepaid TripleSIM Fast 1 m�nad',
            'TA81235 - Telenor Prepaid MBB 10Gb',
            'TA81230 - Telenor Prepaid TripleSIM Halv�r',
            'TA81247 - Prepaid Startpaket HELLO',
                    }
        self.volvo_cards = {'TA81199 - Telenor MBB Volvo 5GB', }
    
    
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
        

    def export_to_excel(self):
        # Alright. We need to create an excel file with a sheet for each type of data. 
        # sheet 1: Longterm for regions
        # sheet 2: Gross adds for regions
        # sheet 3: First charge for regions
        
        # sheet 4: Longterm for each store
        # sheet 5: Gross adds for each store
        # sheet 6: First charge for each store
        
        
        self.long_term_df.to_excel('testingpandas.xlsx')
    
    
    def update_table(self):
        """
        Takes a CSV with updated region/store names from Storecheck, for the period one wants to analyze. 
        Creates a new updated table of all stores which can then be joined with the current database. 
        
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
        
        # Update the Storecheck table with the new data               
        self.cursor.execute("UPDATE Storecheck "
               "INNER JOIN Updated_Store ON Storecheck.Number=Updated_Store.MSISDN "
               "SET Storecheck.Activated = Updated_Store.Activated, Storecheck.Region = Updated_Store.Region, Storecheck.Store = Updated_Store.Store "
               "WHERE Storecheck.Number = Updated_Store.MSISDN;")
        
        startLabel['text'] = "Klar med uppdatering av regioner"  
    
    def calculate_option(self):
        
        
        def create_joined_table_longterm(self):
            """
            Calls relevent SQL queries on the database, to join together the required data for further extraction by other functions.
            """
            
            one_year_earlier = datetime.datetime.strptime(from_cal.get_date(), r"%m/%d/%y") - relativedelta(years=1)
            
            self.cursor.execute(
            'SELECT Laddningsdata.MSISDN, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
            'FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
            'INNER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
            f'WHERE "Topup date" between #{from_cal.get_date()}# and #{to_cal.get_date()}#'
            f'AND Activated between #{one_year_earlier}# and #{to_cal.get_date()}# '
            )          
        
        
        def longterm(self): 
            """
            calculates the longterm/total value of all top ups for a given period. "longterm" is including 
            all top ups on cards less than a year old, including cards getting their first top up.
            """
            
            # Start by making sure the right table is in our cursor, before iterating.
            create_joined_table_longterm(self)

            region_map = Counter()
            region_preloaded_map = Counter()
            store_map = Counter()
            store_preloaded_map = Counter()
            
            for i in self.cursor:
                paid = i.__getattribute__('Amount paid')
                region_map[i.Region] += paid
                store_map[i.Store] += paid
                if i.Artikel in self.preloaded_cards:
                    region_preloaded_map[i.Region] += paid
                    store_preloaded_map[i.Store] += paid
                    
            self.long_term_df = pd.DataFrame.from_dict(region_map, orient='index')
            self.long_term_stores = pd.DataFrame.from_dict(store_map, orient="index")
            
            
        def first_charge(self):
            """
            Calculates the value of first charges for a given period. First charges are those on MSISDNs not top up'ed prior or 
            not top up'ed the last year.
            """
            self.cursor.execute('SELECT * FROM Storecheck '
                                f'WHERE Activated between #{from_cal.get_date()}# and #{to_cal.get_date()}#')
            
            first_dict = {}
            for i in self.cursor:
                first_dict.update({i[0]: {"Region": i[3], "Store": i[5], "Activated": i[2], "Date": "N/A", "Amount": 0}})
            
            
            day_before_from = datetime.datetime.strptime(from_cal.get_date(), r"%m/%d/%y") - relativedelta(days=1)
            
            self.cursor.execute('SELECT MSISDN, "Topup date", "Amount paid" FROM Laddningsdata '
               f'WHERE "Topup date" between #{day_before_from}# and #{to_cal.get_date()}#')
            
            for i in self.cursor:
                if i[0] in first_dict:
                    if first_dict[i[0]]["Date"] == "N/A" or first_dict[i[0]]["Date"] > i[1]:
                        first_dict[i[0]]["Date"] = i[1]
                        first_dict[i[0]]["Amount"] = i[2]
            
            region_first = Counter()
            store_first = Counter()
            for i in first_dict.values():
                region_first[i["Region"]] += i["Amount"]
                store_first[i["Store"]] += i["Amount"]
                
            self.first_region_df = pd.DataFrame.from_dict(region_first, orient="index")   
            self.store_first_df = pd.DataFrame.from_dict(store_first, orient="index")
        
        
        def gross_adds(self):
            """
            Calculates the amount of added RGUs for a given period.
            """
            self.cursor.execute(f'SELECT * FROM Storecheck WHERE Activated between #{from_cal.get_date()}# and #{to_cal.get_date()}#;')
            
            region_gross = Counter()
            store_gross = Counter()
            for i in self.cursor:
                region_gross[i.Region] += 1
                store_gross[i.Store] += 1
                
            self.gross_stores_df = pd.DataFrame.from_dict(store_gross ,orient='index')
            self.gross_regions_df = pd.DataFrame.from_dict(region_gross ,orient='index')
            
                
        # If the attribute exists, a csv has been imported for use and we create an updated table. 
        if hasattr(self, 'csv_path'):
            self.update_table()
            
        
        longterm(self)
        first_charge(self)
        gross_adds(self)
        print(self.long_term_df)
        print("Totalt:" + str(self.long_term_df.sum()))
        
        doneLabel = tk.Label(text="Klar med kalkyl")
        doneLabel.place(x=50, y=350)
        
        


        
        
# Initialize an instance of the DatabaseAnalyzer class.
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

# var = tk.IntVar()
# radio1 = tk.Radiobutton(calculate, text="Regionslista", variable=var, value=1)
# radio2 = tk.Radiobutton(calculate, text="Butikslista", variable=var, value=2)
# radio1.place(x=600, y=50)
# radio2.place(x=600, y=70)
# radioLabel = tk.Label(calculate, text="Välj typ av output").place(x=600, y=20)

importButton = tk.Button(calculate, text="Koppla databas", command=db_analyzer.connect_db, bg="lightblue")
importButton.place(x=20, y=420)
importButton.configure(border=2, relief="raised")

csvButton = tk.Button(calculate, text="Välj csv fil", command=db_analyzer.import_csv, bg="lightblue")
csvButton.place(x=120, y=420)
csvButton.configure(border=2, relief="raised")

calculateButton = tk.Button(calculate, text="Kalkylera", command=db_analyzer.calculate_option, bg="lightblue")
calculateButton.place(x=600, y=200)

exportButton = tk.Button(calculate, text="Exportera", command=db_analyzer.export_to_excel, bg="lightblue")
exportButton.place(x=930, y=200)

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


# En fundering om korten och värde: Om vi tänker att jag laddar ett kort idag, kommer då laddningen in som att den gjordes idag? Och om det
# kortet var nytt, kommer det då dyka upp först imorgon? Att kortet kommer först imorgon är jag rätt hundra på, aktiveringsdatum blir 
# dagen filen laddas upp/skapas och det görs vid kl 8 efterföljande dag. Men hur är det för laddningen? Får den också dagen efter
# som top up date, eller får den dagen som laddningen gjordes? Detta är relevant för hur vi räknar ut i alla fall de första laddningarna.
