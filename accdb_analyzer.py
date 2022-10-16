import pyodbc
import tkinter as tk
from tkinter import filedialog
from tkcalendar import Calendar


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
    if var.get() == 1:
        print("Currently Testing Regionlista")
        # Hämta alla nummer som aktiverats i tidsintervallet
        # cursor.execute(f"SELECT * FROM Storecheck WHERE Activated between #{from_cal.get_date()}# and #{to_cal.get_date()}#;")
        # Hämta all laddningsdata från en specifik tidsintervall
        cursor.execute(f'SELECT * FROM Laddningsdata WHERE "Topup date" between #{from_cal.get_date()}# and #{to_cal.get_date()}#;')
        for i in cursor.fetchall():
            print(i)

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
