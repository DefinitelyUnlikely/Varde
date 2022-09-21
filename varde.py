# What do we want to achieve? First, start by creating a function that reads one file and adds it into the dictionary. We'll 
# work on fixing the rest later. Maybe first of all, we want to actually just figure out how the dictionary should look. 

# So, the current concept I have in mind is quite straigtforward to explain, but perhaps harder to implement. 
# We simply work through each record of the table. We first read the region. We create a top level dictionary for the region
# if one doesn't already exist. We then move forward and add the store for the record. We add that store as a dictionary as well
# within the region dictionary. The store dictionary will then hold a dictionary as well, containing the value and sales keys. Which we increment with 
# the value of the last column for the record and sales which we increment by 1each time the store is seen as a record.
# We might also want to consider adding the value and sales to the region as a whole. Or create a function that 
# calculates this for a given region if we want it. 


from openpyxl import load_workbook
from collections import defaultdict

def main():
    pass

    def read_file():
        workbook = load_workbook("C:\Code\Projects\Varde\9Sep.xlsx")
        worksheet = workbook[workbook.sheetnames[1]]
        region_column = worksheet["D"]
        chain_column = worksheet["E"]
        store_column = worksheet["F"]
        value_column = worksheet["G"]
        for i in zip(region_column[1:], chain_column[1:], store_column[1:], value_column[1:]):
            for j in i:
                print(str(j.value).encode('utf-8'))

    value_dict = defaultdict(dict)
    
    read_file()



if __name__ == '__main__':
    main()