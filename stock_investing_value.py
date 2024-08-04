import csv, sqlite3

class investment():
    def __init__(self, PriceSet):
        self.PriceSet = PriceSet

    def skew(self, PriceSet=False):
        if PriceSet:
            value = len(self.PriceSet)-1
            if self.PriceSet[value]['stdd'] != 0:
                list20 = []
                for a in range(20):
                    list20.insert(0, float(self.PriceSet[value-a]['CloseValue']) - float(self.PriceSet[value-(a+1)]['CloseValue']))
                try:
                    list20.sort()
                    mean20 = sum(list20)/len(list20)
                    med20 = (float(list20[len(list20)//2])+float(list20[(len(list20)//2)+1]))/2
                except:
                    return 'NMV'
                skew = (3*(mean20-med20))/float(self.PriceSet[value]['stdd'])
                return skew
            else:
                return 'STDD0'
        elif not PriceSet:
            value = len(self.PriceSet)-1
            if self.PriceSet[value]['stdd'] != 0:
                list20 = []
                for a in range(20):
                    list20.insert(0, float(self.PriceSet[value-a]['CloseValue']) - float(self.PriceSet[value-(a+1)]['CloseValue']))
                try:
                    list20.sort()
                    mean20 = sum(list20)/len(list20)
                    med20 = (float(list20[len(list20)//2])+float(list20[(len(list20)//2)+1]))/2
                except:
                    return 'NMV'
                skew = (3*(mean20-med20))/float(self.PriceSet[value]['stdd'])
                return skew
            else:
                return 'STDD0'
        else:
            return 'NoPriceSet'

    def timeline(self): # the companies where the starting capital is lower than the near to now closevalues lose money, this is because they are invested in, then cannot afford to trade again thus lose lots of money, such as amazon
        value = len(self.PriceSet)-1
        if (float(self.PriceSet[value]['CloseValue']) > float(self.PriceSet[value]['upperband'])) and (float(self.PriceSet[value-1]['CloseValue']) < float(self.PriceSet[value-1]['upperband'])):
            return 'Buy'
        if (float(self.PriceSet[value]['CloseValue']) < float(self.PriceSet[value]['upperband'])) and (float(self.PriceSet[value-1]['CloseValue']) > float(self.PriceSet[value-1]['upperband'])):
            return 'Sell'
        if (float(self.PriceSet[value]['CloseValue']) > float(self.PriceSet[value]['lowerband'])) and (float(self.PriceSet[value-1]['CloseValue']) < float(self.PriceSet[value-1]['lowerband'])):
            return 'Buy'
        if (float(self.PriceSet[value]['CloseValue']) < float(self.PriceSet[value]['lowerband'])) and (float(self.PriceSet[value-1]['CloseValue']) > float(self.PriceSet[value-1]['lowerband'])):
            return 'Sell'
        if (float(self.PriceSet[value]['CloseValue']) > float(self.PriceSet[value]['upperband'])):
            return 'Above'
        if (float(self.PriceSet[value]['CloseValue']) < float(self.PriceSet[value]['lowerband'])):
            return 'Below'
        try:  
            if float(self.PriceSet[value]['Agradient'])/float(self.PriceSet[value]['CloseValue']) < -2: #this means that if the stock are rapidly falling, they are dropped (more than 2 per 100 closevalue)
                return 'Sell'
        except:
            return None

def get_data(company):
    PriceSet = []
    with open('./stockdata/'+str(company)+'.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
        for item in data:
            PriceSet.append({'Date':item[0],'CloseValue':item[1],'movingAverage':item[2],'Agradient':item[3],'upperband':item[4],'lowerband':item[5],'stdd':item[6]})
        file.close()
    return PriceSet


def doInvestingAuto():
    conn = sqlite3.connect('./userdata/usertradedata.db')
    db = conn.cursor()
    db.execute('SELECT userID FROM users')
    users = db.fetchall()
    for userID in users:
        userID = userID[0]
        db.execute('SELECT stockID, stockmag FROM trades WHERE userID="{}"'.format(userID))
        stockIDs = db.fetchall()
        for stockID in stockIDs:
            stockmag = stockID[1]
            stockID = stockID[0]
            db.execute('SELECT autotrade FROM trades WHERE userID="{}" AND stockID="{}"'.format(userID, stockID))
            toTrade = db.fetchall()[0][0]
            if toTrade == 'True':
                db.execute('SELECT capital FROM users WHERE userID="{}"'.format(userID))
                capital = round(db.fetchall()[0][0],3)
                PriceSet = get_data(stockID)
                test = investment(PriceSet)
                toInvest = test.timeline()
                db.execute('SELECT capital FROM users WHERE userID="{}"'.format(userID))
                currentCapital = float(db.fetchall()[0][0])
                db.execute('SELECT stockmag FROM trades WHERE userID="{}" AND stockID="{}"'.format(userID, stockID))
                currentStockmag = float(db.fetchall()[0][0])
                CurrentCloseValue = float(PriceSet[len(PriceSet)-1]['CloseValue'])
                if toInvest == 'Buy':
                    if float(PriceSet[len(PriceSet)-1]['CloseValue']) < float(PriceSet[len(PriceSet)-1]['movingAverage']) + (float(PriceSet[len(PriceSet)-1]['stdd'])*3): #if the stock has risen above 3 standard deviations, then it has risen to it's maximum value, so dont't invest as it will probally fall
                        if currentCapital - CurrentCloseValue*int((0.1*currentCapital)/CurrentCloseValue) > 0:
                            db.execute('UPDATE users SET capital="{}" WHERE userID="{}"'.format((currentCapital-(CurrentCloseValue*int((0.1*currentCapital)/CurrentCloseValue))),userID))
                            db.execute('UPDATE trades SET stockmag="{}" WHERE userID="{}" AND stockID="{}"'.format(round(currentStockmag + int((0.1*currentCapital)/CurrentCloseValue),1),userID,stockID))
                            conn.commit()
                        else:
                            pass
                elif toInvest == 'Sell':
                    if float(PriceSet[len(PriceSet)-1]['CloseValue']) > float(PriceSet[len(PriceSet)-1]['movingAverage']) - (float(PriceSet[len(PriceSet)-1]['stdd'])*3):
                        if currentStockmag - int((0.1*currentCapital)/CurrentCloseValue) > 0:
                            db.execute('UPDATE users SET capital="{}" WHERE userID="{}"'.format((currentCapital + (CurrentCloseValue*int((0.1*currentCapital)/CurrentCloseValue))),userID))
                            db.execute('UPDATE trades SET stockmag="{}" WHERE userID="{}" AND stockID="{}"'.format(round(currentStockmag - int((0.1*currentCapital)/CurrentCloseValue),1),userID,stockID))
                            conn.commit()
                elif toInvest == 'Above':
                    pass
                elif toInvest == 'Below':
                    pass
                else:
                    pass


doInvestingAuto()
