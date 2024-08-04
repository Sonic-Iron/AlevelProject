from channel_trading import stock_calculation
from datetime import datetime
from datetime import timedelta


def create_test_data(start_date, closevalue, name):
    date = start_date
    PriceSet = []
    for b in range(3):
        for a in range(100):
            if a<= 50:
                closevalue -= (1.2)** a
            else:
                closevalue += (1.2)**a

            date += timedelta(days=1)
            day = date.date()
            PriceSet.append({'Date':str(day),'CloseValue':str(closevalue)})

    return PriceSet


    
        
name = 'TEST1'
PriceSet = create_test_data(datetime(2000,1,1), 1090000000, name)
company = name
for value in PriceSet:
    print(value)
stock_calculation.main(company, None, False, PriceSet)
