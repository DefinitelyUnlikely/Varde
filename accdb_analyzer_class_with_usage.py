import pyodbc
import tkinter as tk
from tkinter import filedialog, ttk
import datetime
from dateutil.relativedelta import relativedelta
import csv
from tkcalendar import Calendar
from collections import Counter, defaultdict
import pandas as pd


class DatabaseAnalyzer():
    
    
    def __init__(self):
        
    
        self.empty_cards = {'TA81218 - Telenor Prepaid TripleSIM 0kr', 'TA81258 - Telenor Prepaid TripleSIM 0kr (till 25-pack)'}
        self.preloaded_cards = {
            'TA81228 - Telenor Prepaid TripleSIM Fast 1 månad Mini',
            'TA81259 - Telenor MBB 100 GB 1 år',
            'TA81220 - Telenor Prepaid TripleSIM Fast 1 månad',
            'TA81235 - Telenor Prepaid MBB 10Gb',
            'TA81230 - Telenor Prepaid TripleSIM Halvår',
            'TA81247 - Prepaid Startpaket HELLO',
            'TA81259 - Telenor prepaid MBB 10GB Arlo',
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
        
        def merge_gross_and_value(self):
            
            #TODO: See to that the renaming actually works. Columns still named Tomma_x etc. 
                       
            self.merged_long_df = pd.merge(self.store_gross_df, self.store_longterm_df, on="Butik", how="inner")
            
            self.merged_long_empty_df = self.merged_long_df[["Tomma_x", "Tomma_y", "Region_x", "Kedja_x"]]
            self.merged_long_empty_df= self.merged_long_empty_df.rename(columns={"Tomma_x": "Gross", "Tomma_y": "Värde"})
            self.merged_long_empty_df.to_excel(writer, sheet_name="Butiker Kombo Tomma")
            
            self.merged_long_loaded_df = self.merged_long_df[["Förladdade_x", "Förladdade_y", "Region_x", "Kedja_x"]]
            self.merged_long_loaded_df = self.merged_long_loaded_df.rename(columns={"Förladdade_x": "Gross", "Förladdade_y": "Värde"})
            self.merged_long_loaded_df.to_excel(writer, sheet_name="Butiker Kombo Förladdade")
            
        def merge_with_chain(self):
            
            # Creating a dataframe with stores and chains.
            # This does create duplicates for stores that has had their chain changed. Not merging with chains
            # removes the duplicates but is pointless, as we wanted the chains as well.
            self.cursor.execute('SELECT DISTINCT Store, Chain FROM Storecheck ')
            data = self.cursor.fetchall()
            self.store_chain_df = pd.DataFrame.from_records(data, columns=['Butik', 'Kedja'], index=['Butik'])
            
            # Merging with existing dataframes
            # self.merged_long_df = pd.merge(self.store_gross_df, self.store_longterm_df, on="Butik", how="inner")

            self.store_longterm_df = pd.merge(self.store_longterm_df,self.store_chain_df, on="Butik", how="inner")
            self.store_first_df = pd.merge(self.store_first_df, self.store_chain_df, on="Butik", how="inner")
            self.store_gross_df = pd.merge(self.store_gross_df, self.store_chain_df, on="Butik", how="inner")
                    
        # First, Merge with chain info
        merge_with_chain(self)
        
        # As we want multiple sheets, I need to create an excel writer.
        file = filedialog.asksaveasfilename(defaultextension=".xlsx")
        with pd.ExcelWriter(file) as writer:
            self.region_longterm_df.to_excel(writer, sheet_name="Långsiktigt Region")
            self.region_first_df.to_excel(writer, sheet_name="Första laddning Region")
            self.region_gross_df.to_excel(writer, sheet_name="Gross Region")
            
            self.store_longterm_df.to_excel(writer, sheet_name="Långsiktigt Butiker")
            self.store_first_df.to_excel(writer, sheet_name="Första laddning Butiker")
            self.store_gross_df.to_excel(writer, sheet_name="Gross Butiker")
              
            merge_gross_and_value(self)
                 
            # Make columns wider, to make the excel file neater from the get go.
            for sheet in writer.sheets:
                worksheet = writer.sheets[sheet]
                worksheet.set_column('A:G', 40)
            
                        
    def update_table(self):
        """
        Takes a CSV with updated region/store names from Storecheck, for the period one wants to analyze. 
        Creates a new updated table of all stores which can then be joined with the current database. 
        """
        
        startLabel = tk.Label(text="Påbörjar uppdatering av regioner")
        startLabel.place(x=50, y=320)
        startLabel.update_idletasks()
        
        # self.cursor.execute('DROP TABLE Updated_Store') # This is needed if the databas already has been used. 
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
        
        self.cursor.commit()
        startLabel['text'] = "Klar med uppdatering av regioner"  
        
    
    def calculate_option(self):     
        
        def longterm(self): 
                    
            # Start by making sure the right table is in our cursor, before iterating.
            one_year_earlier = datetime.datetime.strptime(from_cal.get_date(), r"%m/%d/%y") - relativedelta(years=1)
            
            self.cursor.execute(
            'SELECT Laddningsdata.MSISDN, Store, Storecheck.Region, Activated, "Topup date", Measure, "Amount paid", Artikel '
            'FROM (Laddningsdata INNER JOIN Storecheck ON Laddningsdata.MSISDN=Storecheck.Number) '
            'LEFT OUTER JOIN SIM_kort ON Laddningsdata.MSISDN=SIM_Kort.MSISDN '
            f'WHERE "Topup date" between #{from_cal.get_date()}# and #{to_cal.get_date()}#'
            f'AND Activated between #{one_year_earlier}# and #{to_cal.get_date()}# '
            )    
            
            # I need to add a condition to check for activation date, the SQL command simply lowers the amount of 
            # numbers in the list to the maximum "allowed" by going one year back from the from_date. 
            # i.e. checking that if a number was activated 15/10/23, it's no longer given top ups that's after 15/10/24.

            region_default = defaultdict(Counter)
            store_default = defaultdict(Counter)
            
            for i in self.cursor:
                paid = i.__getattribute__("Amount paid")
                if isinstance(paid, (float, int)):
                    region_default[i.Region]['Totalt'] += paid
                    store_default[i.Store]['Totalt'] += paid
                    
                    if i.Artikel in self.empty_cards:
                        region_default[i.Region]['Tomma'] += paid
                        store_default[i.Store]['Tomma'] += paid
                        store_default[i.Store].setdefault('Region', i.Region)
                    
                    elif i.Artikel in self.preloaded_cards:
                        region_default[i.Region]['Förladdade'] += paid
                        store_default[i.Store]['Förladdade'] += paid
                        store_default[i.Store].setdefault('Region', i.Region)
                    
            self.store_longterm_df = pd.DataFrame.from_dict(store_default, orient='index')[['Tomma', 'Förladdade', 'Totalt', 'Region']]
            self.store_longterm_df.index.name = "Butik"
            self.region_longterm_df = pd.DataFrame.from_dict(region_default, orient='index')[['Tomma', 'Förladdade', 'Totalt']]
            self.region_longterm_df.index.name = "Region"
            
            
        def first_charge(self):
            """
            Calculates the value of first charges for a given period. First charges are those on MSISDNs not top up'ed prior or 
            not top up'ed the last year.
            """
            self.cursor.execute('SELECT Storecheck.Number, Storecheck.Region, Storecheck.Store, Storecheck.Activated, SIM_kort.Artikel FROM Storecheck '
                                'LEFT OUTER JOIN SIM_kort ON Storecheck.Number=SIM_kort.MSISDN '
                                f'WHERE Activated between #{from_cal.get_date()}# and #{to_cal.get_date()}#')
            
            first_dict = {}
            for i in self.cursor:
                first_dict.update({i.Number:
                    {"Region": i.Region, "Store": i.Store, "Activated": i.Activated, "Date": "N/A", "Amount": 0, "Article": i.Artikel}})
            
            
            day_before_from_date = datetime.datetime.strptime(from_cal.get_date(), r"%m/%d/%y") - relativedelta(days=1)
            
            self.cursor.execute('SELECT MSISDN, "Topup date", "Amount paid" FROM Laddningsdata '
                                f'WHERE "Topup date" between #{day_before_from_date}# and #{to_cal.get_date()}#')
            
            for i in self.cursor:
                if i.MSISDN in first_dict:
                    if first_dict[i.MSISDN]["Date"] == "N/A" or first_dict[i.MSISDN]["Date"] > i.__getattribute__('Topup date'):
                        first_dict[i.MSISDN]["Date"] = i.__getattribute__('Topup date')
                        first_dict[i.MSISDN]["Amount"] = i.__getattribute__('Amount paid')
                        
            region_first = Counter()
            store_first = defaultdict(dict)
            for number in first_dict.values():
                if isinstance(number["Amount"], (float, int)):
                    region_first[number["Region"]] += number["Amount"]
                    store_first[number["Store"]].setdefault("Region", number["Region"])
                    store_first[number["Store"]].setdefault("Värde", 0)
                    store_first[number["Store"]]["Värde"] += number["Amount"]
                
            self.store_first_df = pd.DataFrame.from_dict(store_first, orient="index")[['Värde', 'Region']]
            self.store_first_df.index.name = "Butik"
            self.region_first_df = pd.DataFrame.from_dict(region_first, orient="index")
            self.region_first_df.columns = ['Värde']
            self.region_first_df.index.name = "Region"
            
                    
        def gross_adds(self):
            """
            Calculates the amount of added RGUs for a given period.
            """
            self.cursor.execute('SELECT Storecheck.Number, Storecheck.Region, Storecheck.Store, SIM_kort.Artikel FROM Storecheck '
                                'LEFT OUTER JOIN SIM_kort ON Storecheck.Number=SIM_kort.MSISDN '
                                f'WHERE Activated between #{from_cal.get_date()}# and #{to_cal.get_date()}#;')
            
            store_default = defaultdict(Counter)
            region_default = defaultdict(Counter)
            for i in self.cursor:
                store_default[i.Store]["Totalt"] += 1
                region_default[i.Region]["Totalt"] += 1
                
                if i.Artikel in self.empty_cards:
                    store_default[i.Store]["Tomma"] += 1
                    store_default[i.Store].setdefault("Region", i.Region)
                    region_default[i.Region]["Tomma"] += 1

                elif i.Artikel in self.preloaded_cards:
                    store_default[i.Store]["Förladdade"] += 1
                    store_default[i.Store].setdefault("Region", i.Region)
                    region_default[i.Region]["Förladdade"] += 1
                    

            self.store_gross_df = pd.DataFrame.from_dict(store_default, orient="index")[['Tomma', 'Förladdade', 'Totalt', 'Region']]
            self.store_gross_df.index.name = "Butik"
            self.region_gross_df = pd.DataFrame.from_dict(region_default, orient="index")[['Tomma', 'Förladdade', 'Totalt']]
            self.region_gross_df.index.name = "Region" 
            
        
        def usage(self):
            """
            Goes through all numbers to see which ones are still in use. 
            """
            pass
             
        # If the attribute exists, a csv has been imported for use and we create an updated table. 
        if hasattr(self, 'csv_path'):
            self.update_table()
            
        
        longterm(self)
        first_charge(self)
        gross_adds(self)

        doneLabel = tk.Label(text="Klar med kalkyl")
        doneLabel.place(x=50, y=350)
        
        


        
        
# Initialize an instance of the DatabaseAnalyzer class.
# For use in your GUI.
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
Programmet behöver använda MS Access och saknar därmed drivers för UNIX/MacOS. 

2. Ladda ner en kopia av databasen från Workshops VPN. 
"""
instructionsLabel = tk.Label(instructions, bg='gray20', fg='white', text=instructionsText)
instructionsLabel.place(x=50, y=50)


root.mainloop()  
