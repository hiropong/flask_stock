from flask import Flask,flash,redirect,render_template,request,session,abort
from flask_httpauth import HTTPBasicAuth
import os
import sys
# ------------------------------------------------------------------
app = Flask(__name__)
auth=HTTPBasicAuth()
users = {"username":"passwd"}
stock = {}
sales = 0
#------------------------------------------------------------------
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None
#------------------------------------------------------------------
@app.route('/')
def index():
    return render_template("index.html",stock=stock,sales=sales)
#------------------------------------------------------------------
@app.route('/secret/')
@auth.login_required
def home():
    return "Basic Auth"
#------------------------------------------------------------------
@app.route('/calc',methods=['GET','POST'])
def show_user_profile():
    x=request.url
    y=x.split("?")
    z=y[1].replace('%2F','/')
    ans = str(int(eval(z)))
    try:
        return ans
    except:
        return "ERROR"
#------------------------------------------------------------------
@app.route("/stocker")
def check4():
    global stock
    global sales
    function = request.args.get('function')
    name = request.args.get('name')
    amount = request.args.get('amount')
    price = request.args.get('price')

    if function == 'addstock':
        if amount is None:
            amount = 1
        if name not in stock:
            stock[name] = 0
        try:
            stock[name]=int(amount)+int(stock[name])
            return render_template("index.html",stock=stock,sales=sales)
        except:
            return 'ERROR'

    elif function == 'checkstock':
        if name is None:
            mylist = sorted(stock.items())
            a = ""
            for i in range(len(mylist)):
                a += str(mylist[i][0]+": "+str(mylist[i][1])+"\n")
            return a
        else:
            return str(name)+': ' + str(stock[name])

    elif function == 'sell':
        if amount is None:
            amount = 1
        if price is None:
            stock[name]=int(stock[name])-int(amount)
            return render_template("index.html",stock=stock,sales=sales)
        else:
            sales += int(price)*int(amount)
            stock[name]=int(stock[name])-int(amount)
            return render_template("index.html",stock=stock,sales=sales)

    elif function == 'checksales':
        return 'sales: '+str(sales)

    elif function == 'deleteall':
        stock = {}
        sales = 0
        return render_template("index.html",stock=stock,sales=sales)
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True,port=80)
    # app.run(debug=True,host='0.0.0.0',port=80)