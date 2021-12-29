'''
Written: 27/12/2021
27/12/2021 : Starting reader section

Overall Obj: Python script to convert a monthly cvs bank statement to monthly expenditure excel spreadsheet
This part: Takes in dictionary of dictionary and writes a excel sheet formatted like a calander
'''
import Reader
import datetime
import xlsxwriter
from calendar import monthrange
#Setting up format
#------------------------------------------------------------
filepath = input("Please enter filepath: ")
starting_balance_RBC = float(input("Please enter month's RBC starting balance: "))
month, year, transactions = Reader.transactions(filepath)
first_day_weekday, max_day = monthrange(int(year), int(month)) #Num of days in a given month
month_dict={1 : "January",2 : "February",3 : "March",4 : "April",5 : "May",6 : "June",7 : "July",8 : "August",9 : "September",10 : "October",11 : "November",12 : "December"}
week_day_dict = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
workbook = xlsxwriter.Workbook(f'{month_dict[month]}_{str(year)}.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', f'{month_dict[month]} {str(year)}')

#Monday to Sunday
row = 2
column = 4
for day in week_day_dict.values():
    worksheet.write(row, column, day)
    column += 1
#--------------------------------------------------------------


#Writing in data from csv
#--------------------------------------------------------------
last_week_net_RBC_expense = 0
total_expend = 0
row = 3
column = 4+first_day_weekday
#seperate code to start off the starting balance
worksheet.write(4, 1, starting_balance_RBC)

for day in range(1, max_day+1):
    weekday_today = datetime.datetime(year, month, day).weekday()
    if weekday_today == 0: #weeks starting balance is calculated every monday
        starting_balance_RBC += last_week_net_RBC_expense
        last_week_net_RBC_expense = 0
        worksheet.write(row+1,1,starting_balance_RBC)

    if weekday_today == first_day_weekday: #if day is the first day of the month, then it is a new line, so write date, RBC, cash, and description rows.
        worksheet.write(row,3,"Date: ")
        worksheet.write(row,0, "Starting Balances")
        worksheet.write(row+1,0,"RBC: ")
        worksheet.write(row+2,0,"Cash: ")
        worksheet.write(row+3,3,"Description: ")

    worksheet.write(row, column, day) #write the date

    if day in transactions: #if the day has a transaction
        worksheet.write(row+1, column, float(transactions[day]['Amount']))
        last_week_net_RBC_expense += float(transactions[day]['Amount'])
        if float(transactions[day]['Amount']) < 0 and [b[:15] for b in transactions[day]["Description"]] != ['UC Berkely ONLI']: #if it is an expense, add to total expenditure
            total_expend += float(transactions[day]['Amount'])
        if float(transactions[day]["Amount"]) < -50: #if spending is greater than 50 dollars, write in description
            worksheet.write(row+3, column, str([b[:15] for b in transactions[day]["Description"]]))

    if weekday_today == 6: #if it is a sunday, start a new line for the next week, and reset columns
        column = 4
        row +=5
    else:
        column +=1

#write in monthly expenditure
worksheet.write(row+4, 10, "Total Spending")
worksheet.write(row+5, 10, total_expend)
#---------------------------------------------------------------

workbook.close()




