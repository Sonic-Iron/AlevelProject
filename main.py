from flask import Flask, render_template, request, redirect, url_for, session, flash 
from channel_trading import stock_calculation
from sqlite_user_profiles import user_config, create_user, hashing
from stock_investing_value import doInvestingAuto
from optionstaker import option
import csv , re, json # all used to read from files
from datetime import *
app=Flask(__name__)
app.config['SECRET_KEY'] = "45356456$&£(%&(£hkh%K%G£K$£JH%K$JH%658646344%$%G4g3£%£v55£VR$£RBV7£B$£B3-*-+*4"


def get_graph_values(PriceSet):
    datavalues = []
    for value in range(len(PriceSet)):
            datavalues.append({"date":str(PriceSet[value]['Date']),"value":round(float(PriceSet[value]['CloseValue']),2),"uppervalue":round(float(PriceSet[value]['upperband']),2),'lowervalue':round(float(PriceSet[value]['lowerband']),2),'movingAverage':round(float(PriceSet[value]['movingAverage']),2)})
    return(datavalues)
        

def search_check(request):
    if request.form['hidden'] == 'searchbarsub': # the hidden tag is used to check the type of form return
        return True
    return False

def login_check(request):
    if request.form['hidden'] == 'info-enter':
        return 'S'
    elif request.form['hidden'] == 'register':
        return 'R'
    else:
        return False
    
def trade_check(request):
    if request.form['hidden'] == 'trade-enter':
        return True
    return False

def auto_check(request):
    if request.form['hidden'] == 'SwapAuto':
        return True
    return False

def E_check(request):
    if request.form['hidden'] == 'exerciseOption':
        return True
    return False

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def Email_check(email):
    if(re.search(regex,email)):  
        return True  
    return False

def option_check(request):
    if request.form['hidden'] == 'SellOptionsPageSub':
        return 'SO'
    elif request.form['hidden'] == 'BuyOptionsPageSub':
        return 'BO'
    return False

def refresh_check(request):
    if request.form['hidden'] == 'Refresh Stocks':
        return True
    return False

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=['GET','POST'])
def main():
    if request.method == "POST":
        if search_check(request): # checks if the return is a search
            search = request.form['searchbar']
            return redirect("/search/"+str(search))
    return render_template("home.html")


@app.route('/about', methods=["GET", "POST"])
def about():
    if request.method == "POST":
        if search_check(request): # checks if the return is a search
            search = request.form['searchbar']
            return redirect("/search/"+str(search))
    return render_template("about.html")

@app.route('/search/<STOCKID>', methods=["GET", "POST"])
def stockviewer(STOCKID):
    if request.method == "POST":
        try:
            if search_check(request):
                search = request.form['searchbar']
                return redirect("/search/"+str(search))
        except:
            return redirect("/search/")#return nothing

    ISDIGITAL = False
    with open('./digital_currency_list.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == STOCKID:
                ISDIGITAL = True

    if ISDIGITAL == False:            
        PriceSet = stock_calculation.start(str(STOCKID), False)
    if ISDIGITAL == True:
        PriceSet = stock_calculation.start(str(STOCKID), True)
    if PriceSet == "*": #this will be only true if the API fails to find the stock ID or encounters and error
        return render_template('APIfail.html', STOCKID=STOCKID)
    
    dailyprice = PriceSet[len(PriceSet)-1]['CloseValue']


    #ShouldInvest = investment(movingAverage,upperband,lowerband,Agradient,PriceSet)

    datapiecevalues = get_graph_values(PriceSet)
    movingAverage = round(float(PriceSet[len(PriceSet)-1]['movingAverage']),2)
    upperband = round(float(PriceSet[len(PriceSet)-1]['upperband']),2)
    lowerband = round(float(PriceSet[len(PriceSet)-1]['lowerband']),2)
    Agradient = round(float(PriceSet[len(PriceSet)-1]['Agradient']),2)
    dailyprice = round(float(PriceSet[len(PriceSet)-1]['CloseValue']),2)
    if request.method == 'POST':
        if trade_check(request):
            try:
                userID = session['uuid']
            except:
                flash('You are not logged in, please log in to try again')
                return render_template('viewstocks.html',STOCKID=STOCKID,movingAverage=movingAverage,upperband=upperband,lowerband=lowerband,Agradient=Agradient,datapiecevalues=datapiecevalues, dailyprice=dailyprice)        
            stockprice = PriceSet[len(PriceSet)-1]['CloseValue']
            stockID = STOCKID
            stockmag = request.form['stockmag']
            try:
                int(round(float(stockmag)))
            except:
                flash(stockmag+" is not a valid number of stocks to trade")
                return render_template('viewstocks.html',STOCKID=STOCKID,movingAverage=movingAverage,upperband=upperband,lowerband=lowerband,Agradient=Agradient,datapiecevalues=datapiecevalues, dailyprice=dailyprice)
            if user_config.trade_stocks(userID, stockprice, stockID, int(round(float(stockmag)))):
                pass
            else:
                flash("You haven't got enough money, or you don't own enough stocks to buy or sell right now")   
        if refresh_check(request):
            ISDIGITAL = False
            with open('./digital_currency_list.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row[0] == STOCKID:
                        ISDIGITAL = True
            if ISDIGITAL == False:            
                PriceSet = stock_calculation.start(str(STOCKID), False)
            if ISDIGITAL == True:
                PriceSet = stock_calculation.start(str(STOCKID), True)
            if PriceSet == "*": #this will be only true if the API fails to find the stock ID or encounters and error
                return render_template('APIfail.html', STOCKID=STOCKID)
    return render_template('viewstocks.html',STOCKID=STOCKID,movingAverage=movingAverage,upperband=upperband,lowerband=lowerband,Agradient=Agradient,datapiecevalues=datapiecevalues, dailyprice=dailyprice)

@app.route('/log-in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if search_check(request):
            search = request.form['searchbar']
            return redirect("/search/"+str(search))
        elif login_check(request) == 'S': # sign in
            username = request.form['usernamesubbox']
            password = request.form['passwordsubbox']
            user = user_config()
            if user.LogInUser(username, password):
                session['uuid'] = user.userID
                session['permlvl'] = user.get_permlvl(session['uuid'])
                del user
                return redirect('/home')
            else:
                del user
                flash("That's an invalid combination of username and password")
                return render_template('log-in.html')
        else:
            return render_template('log-in.html')
    return render_template('log-in.html')

@app.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if search_check(request):
            search = request.form['searchbar']
            return redirect("/search/"+str(search))
        if login_check(request) == 'R': #regester
            email = request.form['emailsubbox']
            username = request.form['usernamesubbox']
            password = request.form['passwordsubbox']
            passwordcheck = request.form['passwordsubboxsecond']
            create = True
            if password != passwordcheck:
                flash('Your passwords do not match')
                create = False
            if not Email_check(email):
                flash('Your email is invalid')
                create = False
            if create == True:
                if create_user(username, password, email):
                    user = user_config()
                    if user.LogInUser(username, password):
                        session['uuid'] = user.userID
                        session['permlvl'] = user_config.get_permlvl(session['uuid'])
                        del user
                    return render_template('thanksacc.html')
                else:
                    flash('That email is already taken')
                    return render_template('register.html')
            else:
                return render_template('register.html')
    return render_template('register.html')


@app.route('/profile', methods=['GET','POST'])
def user_profile():
    if session.get('uuid') is not None:
        if request.method == 'POST':
            if search_check(request):
                search = request.form['searchbar']
                return redirect("/search/"+str(search))
            if auto_check(request):
                stockID_toggle = request.form['STOCKIDBUTTON']
                user_config.toggle_automation(session['uuid'], stockID_toggle)
            if E_check(request):
                stockID = request.form['hiddenstockID']
                #check for prices
        userStocks = user_config.return_stocks_information(session['uuid'])

        BoptionsSet = option.GetBoughtOptions(session['uuid'])
        BcallsSet = option.GetBoughtCalls(session['uuid'])
        BputsSet = option.GetBoughtPuts(session['uuid'])
        SoptionsSet = option.GetSoldOptions(session['uuid'])
        ScallsSet = option.GetSoldCalls(session['uuid'])
        SputsSet = option.GetSoldPuts(session['uuid'])
        SeOptionsSet = option.GetSellingOptions(session['uuid'])
        SecallsSet = option.GetSellingCalls(session['uuid'])
        SeputsSet = option.GetSellingPuts(session['uuid'])
        
        return render_template('user-prof-page.html',
                               usernamehash=user_config.get_usernamehash(session['uuid']),
                               passwordhash=user_config.get_passwordhash(session['uuid']),
                               userStocks=userStocks,
                               capital=user_config.get_capital(session['uuid']),
                               BoptionsSet=BoptionsSet,
                               BcallsSet=BcallsSet,
                               BputsSet=BputsSet,
                               SoptionsSet=SoptionsSet,
                               ScallsSet=ScallsSet,
                               SputsSet=SputsSet,
                               SeOptionsSet=SeOptionsSet,
                               SecallsSet=SecallsSet,
                               SeputsSet=SeputsSet)
    return redirect('/')
    

@app.route('/logout')
def loggingout():
    if session.get('uuid') is not None:
        if request.method == "POST":
            if search_check(request):
                search = request.form['searchbar']
                return redirect("/search/"+str(search))
        session.pop('uuid')
        session.pop('permlvl')
        return render_template('logout.html')
    return redirect('/')

@app.errorhandler(404)
def error_404(error):
    return redirect('/404')

@app.route('/<path:url>')
def error_url(url):
    if request.method == 'POST':
        if search_check(request):
            search = request.form['searchbar']
            return redirect("/search/"+str(search))
    return render_template('error.html',error=url)
    
@app.route('/update')
def update():
    if session.get('uuid') is not None:
        if float(user_config.get_permlvl(session['uuid'])) > 1:
            return redirect("/")
        doInvestingAuto()
    return redirect("/")

@app.route('/buyOptions', methods=['POST', 'GET'])
def Buyoptions():
    if session.get('uuid') is not None:
        ForSaleCalls = option.GetAllSellingCalls()
        ForSalePuts = option.GetAllSellingPuts()
        if request.method == "POST":
            if search_check(request):
                search = request.form['searchbar']
                return redirect("/search/"+str(search))
            if option_check(request) == 'BO':
                sellID = request.form['hidden-stockinfo']
                NOptBuy = request.form['OBE']
                try:
                    stockToBuy = option.GetSpefSellingOption(sellID)[0] #if the SellingOption no longer exists
                except:
                    return redirect('/buyOptions')
                try:
                    NOptBuy = int(NOptBuy)
                except:
                    flash('Please enter an integer number of options to buy')
                    return redirect('/buyOptions')
                if stockToBuy[6] < NOptBuy:
                    flash('There are not that many options avaliable to buy right now, please enter a lower number')
                    return redirect('/buyOptions')
                if user_config.get_capital(session['uuid']) < float(stockToBuy[4])*100*int(NOptBuy):
                    flash('You do not have enought capital to buy this option')
                    return redirect('/buyOptions')
                option.BuyOption(sellID,
                    stockToBuy[1],
                    stockToBuy[2],
                    session['uuid'],
                    stockToBuy[3],
                    stockToBuy[4],
                    stockToBuy[5],
                    NOptBuy)
                return redirect('/buyOptions')
        return render_template('BuyOptionsPage.html',
                               FSC=ForSaleCalls,
                               FSP=ForSalePuts)
    return redirect('/')

@app.route('/sellOptions', methods=['POST', 'GET'])
def Selloptions():
    if session.get('uuid') is not None:
        if request.method == "POST":
            if search_check(request):
                search = request.form['searchbar']
                return redirect("/search/"+str(search))
            if option_check(request) == 'SO':
                OT = request.form['optionType']
                stockID = request.form['stockID']
                strikePrice = request.form['StrikePrice']
                endDate = '-'.join(request.form['Date'].split('-')[::-1])
                NOpts = request.form['NOpts']
                userID = session['uuid']
                if OT == 'Call': # right to buy stocks from the buyer
                    for value in user_config.return_stocks_information(userID):
                        if stockID in value:
                            if float(value[1]) < 100:
                                flash("You don't have the required assets to carry out this trade")
                                return render_template('SellOptionsPage.html')
                        else:
                            flash("You don't have the required assets to carry out this trade")
                            return render_template('SellOptionsPage.html')
                if OT == 'Put':
                    try:
                        if float(user_config.get_capital(session['uuid'])) <= 100*float(list(csv.reader(open('./stockdata/'+stockID+'.csv', 'r')))[::-1][0][1]):
                            flash("You dont't have the capital to complete the option sale")
                            return render_template('SellOptionsPage.html')
                    except:
                        flash("You don't have the capital to complete the option sale")
                        return render_template('SellOptionsPage.html')
                if int(strikePrice) <= 0:
                    flash("Please enter a strike price above zero")
                    return render_template('SellOptionsPage.html')
                if datetime.strptime(str(endDate), "%d-%m-%Y") < datetime.today():
                    flash("Please enter a future date for the option to expire")
                    return render_template('SellOptionsPage.html')
                if int(NOpts) <= 0:
                    flash("Please enter a number of options to sell above zero")
                    return render_template('SellOptionsPage.html')
                option.SellOption(OT, userID, stockID, strikePrice, endDate, NOpts)
        return render_template('SellOptionsPage.html')
    return redirect('/')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('uuid') is not None:
        if request.method == 'POST':
            if search_check(request):
                search = request.form['searchbar']
                return redirect("/search/"+str(search))
        return render_template('adminpage.html')
    return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=True)
