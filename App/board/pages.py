from flask import Blueprint, render_template,request
from datetime import datetime
from board.database import * 
from board.Patrons import *

bp = Blueprint("pages", __name__)

@bp.route("/", methods = ['POST', 'GET'])
def home():

    customerDetails = []
    result = GetTopBacPatronDetails()
    result2 = []

    if request.method == 'POST':
        result2 = request.form
        for key, value in result2.items():
            customerDetails.append(value)
        result2 = GetPatronDetails('"' + customerDetails[0] + '"')
        temp = result2

    return render_template("pages/home.html", result = result, result2 = result2)

@bp.route("/order",methods = ['POST', 'GET'])
def order():
    orderDetails = []
    orderStatus = ""
    time = None

    if request.method == 'POST':
        result = request.form
        for key, value in result.items():
            orderDetails.append(value)

        patronDetails = GetPatronDetails('"' + orderDetails[0] + '"')

        for row in patronDetails:
            drinks = row[4] + 1
            weight = row[3]
            gender = row[2]
            time = row[6]

        if time is None:
            orderStatus = "INVALID PATRON ID WAS ADDED"
            return render_template("pages/order.html", result2 = orderStatus)

        if time == 0:
            time = datetime.now()
            time = str(time.strftime('%H:%M:%S'))

        time = datetime.strptime(time, "%H:%M:%S")
        timeNow = datetime.now()
        laspedDrink = datetime.strptime(timeNow.strftime('%H:%M:%S'),"%H:%M:%S")

        timePassed = laspedDrink - time
        timePassed = round(timePassed.total_seconds() / 3600)

        lastDrink = datetime.now()
        lastDrink = lastDrink.strftime('%H:%M:%S')

        glassVolume,alcoholLevel = DrinkVolume(orderDetails[1])
        abv = DrinksAbvLevel(glassVolume,alcoholLevel)
        bac = BloodAlcoholConcentration(float(weight),float(abv),gender,timePassed)
        bacLevel = BacLevels(bac)
        
        UpdatePatron('"' + orderDetails[0] + '"',drinks,bac,'"' + lastDrink + '"','"' + str(bacLevel) + '"')
        orderStatus = "ORDER WAS ADDED SUCCESSFULLY"
    return render_template("pages/order.html", result1 = orderStatus)

@bp.route("/admin",methods = ['POST', 'GET'])
def admin():
    newCustomer = []
    patronStatus = ""
    idCheck = None

    if request.method == 'POST':
        result = request.form
        for key, value in result.items():
            newCustomer.append(value)
    
        if len(newCustomer) > 1 :
            AddPatron('"' + newCustomer[1] + '"', '"' + newCustomer[0] + '"', '"' + newCustomer[2] + '"', '"' + newCustomer[3] + '"')
            patronStatus = "PATRON WAS SUCCESSFULLY ADDED"
            return render_template("pages/admin.html", result1 = patronStatus)
        else:

            patronDetails = GetPatronDetails('"' + newCustomer[0] + '"')
            for row in patronDetails:
                idCheck = row[0]

            if idCheck is None:
                patronStatus = "INVALID PATRON ID WAS ADDED"
                return render_template("pages/admin.html", result3 = patronStatus)
            
            DeletePatron('"' + newCustomer[0] + '"')
            patronStatus = "PATRON WAS REMOVED SUCCESSFULLY"
            return render_template("pages/admin.html", result2 = patronStatus)

    return render_template("pages/admin.html")
    
    

