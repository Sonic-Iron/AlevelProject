##WARNING ONLY WORKS ON PYTHON 3.7 or higher

#companies: NVDA, AAPL, MSFT, JPM
#DIGITAL_CURRENCIES: BTC, DOGE
import os, json, requests, csv, sys


class stock_calculation():
    @staticmethod
    def GetData(data, ISDIGITAL):
        prices = []
        if ISDIGITAL == False:
            for a in data:
                if a == 'Note': # the 'note' is the API asking if I want to go premium as the numnber of calls is high for this program
                    return False
                for day, values in data[a].items():
                    if day.startswith('20') or day.startswith('19'):
                        for option, value in values.items():
                            if 'close' in option:
                                tempclose = value
                        prices.insert(0, {'Date':day,'CloseValue':tempclose})
        elif ISDIGITAL == True:
            prices = []
            for a in data:
                if a == 'Note':
                    return False
                for day, values in data[a].items():
                    if day.startswith('20') or day.startswith('19'):
                        for option, value in values.items():
                            if 'close (USD)' in option:
                                tempclose = value
                        prices.insert(0, {'Date':day,'CloseValue':tempclose})
        return prices

    @staticmethod
    def main(company, data, ISDIGITAL, PriceSet=False): #data refers to the stock name request, priceset here is the closevalues and dates 
        if PriceSet == False:
            PriceSet = stock_calculation.GetData(data, ISDIGITAL)
            if PriceSet == False:
                return '*'
        else:
            pass
        with open('./stockdata/'+str(company)+'.csv', 'w', newline='') as file:
            stock_data_writer = csv.writer(file)
            for point in range(len(PriceSet)):
                if point>20:
                    movingAverage = 0
                    for N in range(20):
                        movingAverage = movingAverage + float(PriceSet[point-(1+N)]['CloseValue']) #calculting average
                    movingAverage = movingAverage/20
                    variance = 0
                    for N in range(20):
                        variance = variance + ((float(PriceSet[point-(1+N)]['CloseValue'])-movingAverage)**2) #calculting standard deviation
                    variance = variance/19
                    STDD = variance**0.5
                    upperband = movingAverage + (2*STDD)
                    lowerband = movingAverage - (2*STDD)

                    gradient5 = (float(PriceSet[point-1]['CloseValue'])-float(PriceSet[point-6]['CloseValue']))/5
                    gradient2 = (float(PriceSet[point-1]['CloseValue'])-float(PriceSet[point-3]['CloseValue']))/2

                    Agradient = (gradient5/2)+gradient2 # make a proper weighted graident
                    stock_data_writer.writerow([PriceSet[point]['Date'],PriceSet[point]['CloseValue'],movingAverage,Agradient,upperband,lowerband,STDD])
                else:
                    stock_data_writer.writerow([PriceSet[point]['Date'],PriceSet[point]['CloseValue'],PriceSet[point]['CloseValue'],PriceSet[point]['CloseValue'],PriceSet[point]['CloseValue'],PriceSet[point]['CloseValue'],'0'])     
        file.close()
        PriceSet = []
        with open('./stockdata/'+str(company)+'.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
            for item in data:
                PriceSet.append({'Date':item[0],'CloseValue':item[1],'movingAverage':item[2],'Agradient':item[3],'upperband':item[4],'lowerband':item[5],'stadd':item[6]})
        file.close()
        return PriceSet

    @staticmethod
    def start(company, ISDIGITAL, UPDATE=True):
        if (os.path.exists('./stockdata/'+str(company)+'.csv')) and (UPDATE == False):
            PriceSet = []
            with open('./stockdata/'+str(company)+'.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
                for item in data:
                    PriceSet.append({'Date':item[0],'CloseValue':item[1],'movingAverage':item[2],'Agradient':item[3],'upperband':item[4],'lowerband':item[5],'stadd':item[6]})
            file.close()
            return PriceSet
        else:
            api_key = '4KMUR9F881V1L3MA' #obscure this
            web = "https://www.alphavantage.co/query?"
            timedelay = "TIME_SERIES_DAILY"
            outputsize='full'
            try:
                if ISDIGITAL == False:
                    path = "function=TIME_SERIES_DAILY&symbol="+str(company)+'&outputsize='+outputsize+'&apikey='+str(api_key) # has data for the path that I want to request
                    r = requests.get(web+path+api_key)
                    data = r.json()
                    if list(data)[0].startswith('Error'): #if the STOCKID is invalid (such as not real), the API throws an error
                        print(data)
                        return '*'
                elif ISDIGITAL == True:
                    path = "function=DIGITAL_CURRENCY_DAILY&symbol="+str(company)+'&market=USD&apikey='+str(api_key) # has data for the path that I want to request
                    r = requests.get(web+path+api_key)
                    data = r.json()
                    if list(data)[0].startswith('Error'): #if the STOCKID is invalid (such as not real), the API throws an error
                        return '*'
            except Exception as e:
                print("The connection to the API failed, try reconnecting to the internet")
                print(e)
                return '*'
            try:
                if data:
                    PriceSet = stock_calculation.main(company, data, ISDIGITAL)
            except Exception as e:
                print(e)
                return '*'
        return PriceSet