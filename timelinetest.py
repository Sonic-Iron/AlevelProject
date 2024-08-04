import csv

stockIDs = ['MSFT','NVDA','INTL','SHOP','SBUX','JPM','DOW','VIAV','TSLA']

def get_data(company):
    PriceSet = []
    with open('./stockdata/'+str(company)+'.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
        for item in data:
            PriceSet.append({'Date':item[0],'CloseValue':item[1],'movingAverage':item[2],'Agradient':item[3],'upperband':item[4],'lowerband':item[5],'stdd':item[6]})
        file.close()
    return PriceSet

for a in stockIDs:
    PriceSet = get_data(a)
    currentCapital = 1000
    currentStockmag = 0
    for value in range(len(PriceSet)-1):
        CurrentCloseValue = float(PriceSet[len(PriceSet)-1]['CloseValue'])
        if (float(PriceSet[value]['CloseValue']) > float(PriceSet[value]['upperband'])) and (float(PriceSet[value-1]['CloseValue']) < float(PriceSet[value-1]['upperband'])):
            currentCapital -= (CurrentCloseValue*int((0.1*currentCapital)/CurrentCloseValue))
            currentStockmag = round(currentStockmag + int((0.1*currentCapital)/CurrentCloseValue),1)
        if (float(PriceSet[value]['CloseValue']) < float(PriceSet[value]['upperband'])) and (float(PriceSet[value-1]['CloseValue']) > float(PriceSet[value-1]['upperband'])):
            currentCapital += (CurrentCloseValue*int((0.1*currentCapital)/CurrentCloseValue))
            currentStockmag = round(currentStockmag - int((0.1*currentCapital)/CurrentCloseValue),1)
        if (float(PriceSet[value]['CloseValue']) > float(PriceSet[value]['lowerband'])) and (float(PriceSet[value-1]['CloseValue']) < float(PriceSet[value-1]['lowerband'])):
            currentCapital -= (CurrentCloseValue*int((0.1*currentCapital)/CurrentCloseValue))
            currentStockmag = round(currentStockmag + int((0.1*currentCapital)/CurrentCloseValue),1)
        if (float(PriceSet[value]['CloseValue']) < float(PriceSet[value]['lowerband'])) and (float(PriceSet[value-1]['CloseValue']) > float(PriceSet[value-1]['lowerband'])):
            currentCapital += (CurrentCloseValue*int((0.1*currentCapital)/CurrentCloseValue))
            currentStockmag = round(currentStockmag - int((0.1*currentCapital)/CurrentCloseValue),1)
        if (float(PriceSet[value]['CloseValue']) > float(PriceSet[value]['upperband'])):
            pass
        if (float(PriceSet[value]['CloseValue']) < float(PriceSet[value]['lowerband'])):
            pass
        try:  
            if float(PriceSet[value]['Agradient'])/float(PriceSet[value]['CloseValue']) < -2: #this means that if the stock are rapidly falling, they are dropped (more than 2 per 100 closevalue)
                currentCapital += (CurrentCloseValue*int((0.1*currentCapital)/CurrentCloseValue))
                currentStockmag = round(currentStockmag - int((0.1*currentCapital)/CurrentCloseValue),1)
        except:
            pass
    currentCapital += currentStockmag * float(PriceSet[len(PriceSet)-1]['CloseValue'])
    currentStockmag = 0
    print(a, currentCapital-100, currentStockmag)



    
