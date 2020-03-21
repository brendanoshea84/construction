import os
from tkinter import *
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from tkinter import messagebox

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone3"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# Welcome Page
# Sign in for new members with a pre password
# Login using your own password
@app.route('/', methods=['POST', 'GET'])
@app.route('/intro', methods=['POST', 'GET'])
def sign_in():   
    # Sign in for new members with a pre password
    if request.method == 'POST':
        try_pass = request.form.get('new_password')
        w_password = mongo.db.welcome_password.find_one()
        for key, val in w_password.items():
            if 'welcome_password' in key:
                wel_pass = val
        if wel_pass == try_pass:
            # If sussecful- Page to input new member info
            print("testing wel_pass == try_pass")
            return redirect(url_for('new_member_info'))
        else:
            print("error at new member")
            return redirect(url_for('error_new'))
    return render_template('intro.html', employees=mongo.db.employees.find(), welcomes=mongo.db.welcome_password.find())       

def login():  
    # Login using your own password
    if request.method == 'POST':
        # User can use they name or employee number
        employees = mongo.db.employees
        login_user =  employees.find_one({'employee_username' : request.form.get('login')}) or employees.find_one({'employee_number' : request.form.get('login')})
         
        login_pass = request.form.get('password_user')

        if login_user:
            if login_pass == login_user['employ_password']:
                print("testing login area")
                session['login_user'] = request.form['login']
                print(session)
                print('session')
                return redirect(url_for('base'))
            else:
                print("error at login")
                return redirect(url_for('error_existing'))
                
              
   
    return render_template('intro.html', employees=mongo.db.employees.find(), welcomes=mongo.db.welcome_password.find())       








@app.route('/base')
def base():
    print ("working at base")
    return render_template("base.html")

@app.route('/error_new')
def error_new():
    
    return render_template("error_new.html")

@app.route('/error_existing')
def error_existing():
    
    return render_template("error_existing.html")




@app.route('/new_member_info', methods=['POST', 'GET'])   
def new_member_info():
    if request.method == 'POST':
        print ("working at new_member_info")
    return render_template("new_member_info.html")    

if __name__ == '__main__':
    app.secret_key='1234'
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)  