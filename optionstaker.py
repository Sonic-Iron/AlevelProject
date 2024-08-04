import sqlite3, time
from datetime import datetime
from sqlite_user_profiles import user_config

class option():

    @staticmethod
    def BuyOption(sellingDatabaseID, optionType, sellerID, userID, stockID, strikePrice, endDate, NOpts):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        print(userID, sellerID)
        user_config.modify_capital(userID, 100*NOpts*strikePrice*-1)
        user_config.modify_capital(sellerID, 100*NOpts*strikePrice)
        db.execute('INSERT INTO BoughtOptions VALUES (NULL, ?, ?, ? ,?, ? ,? ,?)', (optionType, sellerID, userID, stockID, strikePrice, endDate, NOpts))
        db.execute('SELECT NOpts FROM SellingOptions WHERE optionSID="{}"'.format(sellingDatabaseID))
        CNOpts = int(db.fetchall()[0][0]) #there should only be one value
        db.execute('UPDATE SellingOptions SET NOpts="{}" WHERE optionSID="{}"'.format(CNOpts-NOpts,sellingDatabaseID))      
        db.execute('DELETE FROM SellingOptions WHERE Nopts<=0')
        conn.commit()
        conn.close()
        
    @staticmethod
    def SellOption(optionType, userID, stockID, strikePrice, endDate, NOpts):
        if optionType == 'Put':# sell if the market is going to rise
            conn = sqlite3.connect('./userdata/usertradedata.db')
            db = conn.cursor()
            db.execute("INSERT INTO SellingOptions VALUES (NULL,'Put',?,?,?,?,?)",(userID,stockID, strikePrice, endDate, NOpts))
            conn.commit()
            conn.close()
            return True
        elif optionType == 'Call':# sell if market is going to fall
            conn = sqlite3.connect('./userdata/usertradedata.db')
            db = conn.cursor()
            db.execute("INSERT INTO SellingOptions VALUES (NULL,'Call',?,?,?,?,?)",(userID,stockID, strikePrice, endDate, NOpts))
            conn.commit()
            conn.close()
            return True
        else:
            return False            

    # buying a stock:
    # put is right to sell stocks at a price
    # calls is right to buy stocks at a price

    #all the options that are being traded
    
    @staticmethod
    def GetAllBoughtOptions():
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionsBID, type, stockVol, strikePrice, premium, endDate FROM BoughtOptions')
        options = db.fetchall()
        conn.close()
        return options
    
    @staticmethod
    def GetAllBoughtCalls(): # right to buy at a price
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionsBID,stockID, strikePrice, premium, endDate, NOpts FROM BoughtOptions WHERE type="{}"'.format('Calls'))
        Calls = db.fetchall()
        conn.close()
        return Calls
    
    @staticmethod   
    def GetAllBoughtPuts(): # right to sell at a price
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionBID,stockID, strikePrice, premium, endDate, NOpts FROM BoughtOptions WHERE type="{}"'.format('Puts'))
        Puts = db.fetchall()
        conn.close()
        return Puts
        
    @staticmethod
    def GetBoughtOptions(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionBID,type, stockID, strikePrice, endDate, NOpts FROM BoughtOptions WHERE userIDB={}'.format(userID))
        options = db.fetchall()
        conn.close()
        return options
    
    @staticmethod
    def GetBoughtCalls(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionBID,stockID, strikePrice, endDate, NOpts FROM BoughtOptions WHERE type="{}" AND userIDB="{}"'.format('Call', userID))
        MyCalls = db.fetchall()
        conn.close()
        return MyCalls

    @staticmethod
    def GetBoughtPuts(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionBID,stockID, strikePrice, endDate, NOpts FROM BoughtOptions WHERE type="{}" AND userIDB="{}"'.format('Put', userID))
        MyPuts = db.fetchall()
        conn.close()
        return MyPuts

    # all the options the user has sold
        
    @staticmethod
    def GetSoldOptions(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionBID,type, stockID, strikePrice, endDate, NOpts FROM BoughtOptions WHERE userIDS={}'.format(userID))
        options = db.fetchall()
        conn.close()
        return options
    
    @staticmethod
    def GetSoldCalls(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionBID,stockID, strikePrice, endDate, NOpts FROM BoughtOptions WHERE type="{}" AND userIDS="{}"'.format('Call', userID))
        MyCalls = db.fetchall()
        conn.close()
        return MyCalls

    @staticmethod
    def GetSoldPuts(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionBID,stockID, strikePrice, endDate, NOpts FROM BoughtOptions WHERE type="{}" AND userIDS="{}"'.format('Put', userID))
        MyPuts = db.fetchall()
        conn.close()
        return MyPuts

    # options user is trying to sell

    @staticmethod
    def GetAllSellingOptions():
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionSID, type, stockID, strikePrice, endDate, NOpts FROM SellingOptions ')
        Options = db.fetchall()
        conn.close()
        return Options

    @staticmethod
    def GetAllSellingCalls():
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionSID, stockID, strikePrice, endDate, NOpts FROM SellingOptions WHERE type="{}" '.format('Call'))
        SCalls = db.fetchall()
        conn.close()
        return SCalls

    @staticmethod
    def GetAllSellingPuts():
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionSID, stockID, strikePrice, endDate, NOpts FROM SellingOptions WHERE type= "{}"'.format('Put'))
        SPuts = db.fetchall()
        conn.close()
        return SPuts

    @staticmethod
    def GetSellingOptions(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionSID, type, stockID, strikePrice, endDate, NOpts FROM SellingOptions WHERE userID="{}"'.format(userID))
        SOptions = db.fetchall()
        conn.close()
        return SOptions

    @staticmethod
    def GetSellingCalls(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionSID, stockID, strikePrice, endDate, NOpts FROM SellingOptions WHERE type="{}" AND userID="{}"'.format('Call', userID))
        SCalls = db.fetchall()
        conn.close()
        return SCalls

    @staticmethod
    def GetSellingPuts(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionSID, stockID, strikePrice, endDate, NOpts FROM SellingOptions WHERE type= "{}" AND userID="{}"'.format('Put', userID))
        SPuts = db.fetchall()
        conn.close()
        return SPuts


    @staticmethod
    def GetSpefSellingOption(SellingOptionID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT * FROM SellingOptions WHERE optionSID = "{}"'.format(SellingOptionID))
        SSO = db.fetchall()
        conn.close()
        return SSO

    @staticmethod
    def GetSpefBoughtOption(SellingOptionID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT * FROM BoughtOptions WHERE optionSID = "{}"'.format(SellingOptionID))
        SSO = db.fetchall()
        conn.close()
        return SSO
    
    @staticmethod
    def ExecuteOptionAuto():
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT optionsBID, endDate FROM BoughtOptions')
        bDates = db.fetchall()
        db.execute('SELECT optionsSID, endDate FROM SellingOptions')
        sDates = db.fetcall()
        for dateSet in sDates:
            if datetime.strptime(str(dateSet[1]), "%d-%m-%Y") <= datetime.today():
                db.execute('DELETE FROM SellingOptions WHERE optionsSID="{}"'.format(dateSet[0]))
        for dateSet in bDates:
            if datetime.strptime(str(dateSet[1]), "%d-%m-%Y") <= datetime.today():
                db.execute('SELECT * FROM BoughtOptions WHERE optionsBID="{}"'.format(dateSet[0]))
                Bset = db.fetchall()
                for Bout in Bset:
                    userSID = Bout[2]
                    userBID = Bout[3]
                    if Bout[1] == 'Call':
                        db.execute("INSERT INTO trades VALUES(NULL, ?, ?, ?, 'False', ?)",userBID, Bout[4], Bout[6], datetime.today().strftime('%d-%m-%Y'))
                        
                

