import pandas as pd


csv_file = pd.read_csv("Projects\Varde\Analysis - topup.csv", converters={'MSISDN': str})   # Convert to keep leading zero. Might not be neccesery. 

for index, row in csv_file.iterrows():
    print(row["MSISDN"], row["Amount paid"])