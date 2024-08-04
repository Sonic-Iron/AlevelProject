import csv, os, time
from channel_trading import stock_calculation
from stock_investing_value import doInvestingAuto
from optionstaker import option

def autoinvesting(stockIDs = []):
    if len(stockIDs) == 0:
        index = 0
        for file in os.listdir('./stockdata'):
            index += 1
            if index == 5:
                print('sleeping')
                time.sleep(61)
                index = 1
            STOCKID = str(file).strip('.csv')
            with open('./digital_currency_list.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row[0] == STOCKID:
                        ISDIGITAL = True
                ISDIGITAL = False
            print(STOCKID, ISDIGITAL)
            stock_calculation.start(str(STOCKID), ISDIGITAL, UPDATE=True)
    else:
        index = 0
        for file in stockIDs:
            index += 1
            if index == 5:
                print('sleeping')
                time.sleep(61)
                index = 1
            if file.endswith('.csv'):
                STOCKID = str(file).strip('.csv')
            with open('./digital_currency_list.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row[0] == STOCKID:
                        ISDIGITAL = True
                ISDIGITAL = False
            print(STOCKID, ISDIGITAL)
            stock_calculation.start(str(STOCKID), ISDIGITAL, UPDATE=True)
while True:
    autoinvesting()
    doInvestingAuto()
    option.ExecuteOptionAuto()
    time.sleep(86400)

