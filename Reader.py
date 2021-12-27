'''
Written: 27/12/2021
27/12/2021 : Starting reader section

Overall Obj: Python script to convert a monthly cvs bank statement to monthly expenditure excel spreadsheet
This part: Returns month and dictionary with key == day of month, with value as a dictionary of "Amount" and "Description"
'''

import csv
def transactions(filepath):
    #First two lines of RBC csvfile are empty
    csvfile = open(filepath, newline='')
    next(csvfile)
    next(csvfile)

    #Transaction dictionary with key = day of month
    transaction_dicts_by_day = {}
    month = 0
    year = 0
    reader = csv.DictReader(csvfile)
    for row in reader:
        day = int(row['Transaction Posted Date'][3:5])
        #assigns month and year only once
        if not month or year:
            month = int(row['Transaction Posted Date'][:2])
            year = int(row['Transaction Posted Date'][-4:])
        #Only really care about Amount and Description, so create new dictionary with only those things
        if day in transaction_dicts_by_day.keys(): #if there are multiple expenses on the same day
            transaction_dicts_by_day[day]['Amount'] = str(float(transaction_dicts_by_day[day]['Amount']) + float(row['Amount']))
            transaction_dicts_by_day[day]['Description'].append(row["Description"])
        else:
            transaction_dicts_by_day[day] = {'Amount':row['Amount'], 'Description':[row['Description']]}
    
    csvfile.close()
    return month, year, transaction_dicts_by_day



