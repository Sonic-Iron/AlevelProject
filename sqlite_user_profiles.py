import sqlite3
from datetime import datetime
import smtplib
from email.message import EmailMessage

class user_config:
    def __init__(self):
        pass
        
    def LogInUser(self, username, password):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        sqlusername = user_config.rehash(username)
        while '"' in sqlusername:
            sqlusername.replace('"', "'")
        sqlpassword = user_config.rehash(password)
        while '"' in sqlpassword:
            sqlpassword.replace('"', "'")
        db.execute('SELECT userID FROM users WHERE usernamehash="{}" AND passwordhash="{}"'.format(sqlusername, sqlpassword))
        if len(db.fetchall()) == 0:
            conn.close()
            return False
        else:
            self.userID = db.fetchall()
            conn.close()
            return True

    @staticmethod
    def rehash(to_hash):
        hashed = to_hash + '::hash'
        return hashed

    @staticmethod
    def get_usernamehash(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT usernamehash FROM users WHERE userID="{}"'.format(userID))
        username = db.fetchall()[0][0]
        conn.close()
        return username

    @staticmethod
    def set_username(userID, new_username):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        new_usernamehash = user_config.rehash(new_usernamehash)
        db.execute('UPDATE users SET usernamehash="{}" WHERE userID="{}"'.format(new_usernamehash, userID))
        conn.commit()
        conn.close()

    @staticmethod
    def get_passwordhash(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT passwordhash FROM users WHERE userID="{}"'.format(userID))
        password = db.fetchall()[0][0]
        conn.close()
        return password

    @staticmethod
    def set_passwordhash(userID, new_password):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        new_passwordhash = user_config.rehash(new_password)
        db.execute('UPDATE users SET passwordhash="{}" WHERE userID="{}"'.format(new_passwordhash, userID))
        conn.commit()
        conn.close()

    @staticmethod
    def get_email(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT email FROM users WHERE userID="{}"'.format(userID))
        email = db.fetchall()[0][0]
        conn.close()
        return email

    @staticmethod
    def set_email(userID, new_email):
        new_email = str(new_email)
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('UPDATE users SET email="{}" WHERE userID="{}"'.format(new_email, userID))
        conn.commit()
        conn.close()

    @staticmethod
    def get_permlvl(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT permissionslevel FROM users WHERE userID="{}"'.format(userID))
        print(db.fetchall())
        permslvl = db.fetchall()[0]
        conn.close()
        return permslvl

    @staticmethod
    def set_permlvl(userID, new_lvl):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('UPDATE users SET permissionslevel="{}" WHERE userID="{}"'.format(new_lvl, userID))
        conn.commit()
        conn.close()

    @staticmethod
    def modify_permlvl(userID, delta_lvl):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT permissionslevel FROM users WHERE userID="{}"'.format(userID))
        current_lvl = db.fetchall()[0][0]
        db.execute('UPDATE users SET permissionslevel="{}" WHERE userID="{}"'.format((current_lvl+delta_lvl),userID))
        conn.commit()
        conn.close()

    @staticmethod
    def get_capital(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT capital FROM users WHERE userID="{}"'.format(userID))
        capital = round(db.fetchall()[0][0], 4)
        conn.close()
        return capital
        
    @staticmethod
    def set_capital(userID, new_cap):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('UPDATE users SET capital ="{}" WHERE userID="{}"'.format(new_cap, userID))
        conn.commit()
        conn.close()

    @staticmethod
    def modify_capital(userID, mod_cap):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT capital FROM users WHERE userID="{}"'.format(userID))
        capital = db.fetchall()[0][0]
        db.execute('UPDATE users SET capital="{}" WHERE userID="{}"'.format((capital+mod_cap), userID))
        conn.commit()
        conn.close()

    @staticmethod
    def get_stocks(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT stockID,stockmag FROM users WHERE userID="{}"'.format(userID))
        conn.close()

    @staticmethod
    def search_stocks_selling(stockID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT * FROM SellingOptions WHERE stockID="{}"'.format(stockID))
        conn.close()
        

    @staticmethod
    def trade_stocks(userID, stockprice, stockID, stockmag):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT capital FROM users WHERE userID="{}"'.format(userID))
        cap = db.fetchall()[0][0]
        db.execute('SELECT stockmag FROM trades WHERe userID="{}" AND stockID="{}"'.format(userID, stockID))
        user_config.modify_capital(userID, 10000000)
        if len(db.fetchall()) == 0:
            if int(stockmag) > 0:
                if cap >= (float(stockprice)*float(stockmag)):
                    db.execute('INSERT INTO trades VALUES (NULL, ?,?,?, "False", ?)',(userID, stockID, stockmag,datetime.today().strftime('%d-%m-%Y')))
                    conn.commit()
                    conn.close()
                    user_config.modify_capital(userID, (-1*float(stockprice)*float(stockmag)))
                    return True
                else:
                    return False
            else:
                return False
        elif int(stockmag) > 0:
            if int(stockmag)*float(stockprice) <= float(cap):
                cost = float(stockmag) * float(stockprice)
                db.execute('SELECT stockmag FROM trades WHERE stockID="{}" AND userID="{}"'.format(stockID, userID))
                current_stockmag = db.fetchall()[0][0]
                new_stockmag = int(round(float(current_stockmag))) + int(stockmag)
                db.execute('UPDATE trades SET stockmag="{}" WHERE userID="{}" AND stockID="{}"'.format(new_stockmag,userID,stockID))
                db.execute('UPDATE trades SET date="{}" WHERE userID="{}" AND stockID="{}"'.format(datetime.today().strftime('%d-%m-%Y'), userID, stockID))
                conn.commit()
                conn.close()
                user_config.modify_capital(userID,(-1*cost))
                return True
            else:
                return False
        elif int(stockmag) < 0:
            db.execute('SELECT stockmag FROM trades WHERE stockID="{}" AND userID="{}"'.format(stockID, userID))
            current_stockmag = db.fetchall()[0][0]
            if int(round(float(current_stockmag))) + int(stockmag) >= 0:
                db.execute('UPDATE trades SET stockmag="{}" WHERE userID="{}" AND stockID="{}"'.format((int(round(float(current_stockmag))) + int(stockmag)), userID, stockID))
                db.execute('UPDATE trades SET date="{}" WHERE userID="{}" AND stockID="{}"'.format(datetime.today().strftime('%d-%m-%Y'), userID, stockID))
                rev = (-1*int(stockmag)) * float(stockprice)
                db.execute('SELECT stockmag FROM trades WHERE userID="{}" AND stockID="{}"'.format(userID, stockID))
                count = db.fetchall()[0][0]
                if count == '0':
                    db.execute('DELETE FROM trades WHERE userID="{}" AND stockID="{}"'.format(userID, stockID))
                conn.commit()
                conn.close()
                user_config.modify_capital(userID, rev)
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def return_stocks_information(userID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT stockID, stockmag, autotrade, date FROM trades WHERE userID="{}"'.format(userID))
        stocks = db.fetchall()
        conn.close()
        return stocks

    def toggle_automation(userID, stockID):
        conn = sqlite3.connect('./userdata/usertradedata.db')
        db = conn.cursor()
        db.execute('SELECT autotrade FROM trades WHERE userID="{}" AND stockID="{}"'.format(userID, stockID))
        mode = db.fetchall()[0][0]
        if str(mode) == 'False':
            db.execute('UPDATE trades SET autotrade="True" WHERE userID="{}" AND stockID="{}"'.format(userID, stockID))
        elif str(mode) == 'True':
            db.execute('UPDATE trades SET autotrade="False" WHERE userID="{}" AND stockID="{}"'.format(userID, stockID))
        conn.commit()
        conn.close()
            
def create_user(username, password, email): # when the user first registers, this is executed
    conn = sqlite3.connect('./userdata/usertradedata.db')
    db = conn.cursor()
    usernamehash = hashing(username)
    passwordhash = hashing(password)
    db.execute('SELECT usernamehash FROM users WHERE usernamehash="{}"'.format(email, usernamehash))
    if len(db.fetchall()) != 0:
        conn.close()
        return False
    else:
        db.execute("INSERT INTO users VALUES(NULL, ?,?,?,'0',0)",(usernamehash, passwordhash, email))
        conn.commit()
        conn.close()
        return True
    
    
    
    

def hashing(to_hash):
    hashed = to_hash + '::hash' # create or find a hashing algorithm in the future
    return hashed


def main():
    conn = sqlite3.connect('./userdata/usertradedata.db')
    db = conn.cursor()
    db.execute("SELECT name FROM sqlite_master where type='table'")
    tables = db.fetchall()
    if len(tables) != 4 or True:
        tables2 = []
        for table in tables:
            tables2.append(table[0])
        tables = tables2
        if 'users' not in tables:
            db.execute('CREATE TABLE users (userID INTEGER PRIMARY KEY, usernamehash TEXT, passwordhash TEXT, email TEXT, permissionslevel INTEGER, capital REAL)')
        if 'trades' not in tables:
            db.execute('CREATE TABLE trades (tradeID INTEGER PRIMARY KEY, userID INTEGER, stockID TEXT, stockmag TEXT, autotrade TEXT, date TEXT)')
        if 'SellingOptions' not in tables:
            db.execute('CREATE TABLE SellingOptions (optionSID INTEGER PRIMARY KEY, type TEXT, userID INTEGER, stockID TEXT, strikePrice REAL, endDate TEXT, NOpts INTEGER)')
        if 'BoughtOptions' not in tables:
            db.execute('CREATE TABLE BoughtOptions (optionBID INTEGER PRIMARY KEY, type TEXT, userIDS INTEGER, userIDB, stockID TEXT, strikePrice REAL, endDate TEXT, NOpts INTEGER)')
    # call - right to buy at the strike price, bets on the market rising
    # put - right to sell at the strike price, bets on the market falling
        print("Created Tables")
    else:
        pass


if __name__ == "__main__":
    main()

