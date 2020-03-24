import os
from tkinter import *
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from tkinter import messagebox as mb

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone3"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# Welcome Page
# Sign in for new members with a pre password
# Login using your own password
@app.route('/', methods=['POST', 'GET'])
@app.route('/intro', methods=['POST', 'GET'])
def intro(): 
    if request.method == 'POST': 
    # Sign in for new members with a pre password
        if 'new_member_btn' in request.form:
            print("testing")

            global new_first_name
            new_first_name = request.form.get('new_member_first')


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
                mb.showinfo("Incorrect Password", "Your welcome password is incorrect, please contact your supervisor! Welcome Password for CODE INSTITUTE: "+ wel_pass)
                print("welcome password ")
        else:
    # Login using your own password
        # User can use they name or employee number
            global login_user
            employees = mongo.db.employees
            login_user =  employees.find_one({'employee_username' : request.form.get('login')}) or employees.find_one({'employee_number' : request.form.get('login')})
            login_pass = request.form.get('password_user')

            if login_user:
                if login_pass == login_user['employ_password']:
                    print("testing login area")
                    session['login_user'] = request.form['login']
                    print(session)
                    print('session')
                    return redirect(url_for('main'))
                else:
                    print("error at login")
                    return redirect(url_for('error_existing'))
                
              
   
    return render_template('intro.html', employees=mongo.db.employees.find(), welcomes=mongo.db.welcome_password.find())       


@app.route('/main', methods=['GET'])
def main():
    print ("going to main")
    print(login_user)
    return render_template("main.html", testing=login_user)





@app.route('/base', methods=['POST', 'GET'])
def base():
    print ("working at base")
    return render_template("base.html")



@app.route('/error_existing')
def error_existing():
    
    return render_template("error_existing.html")




@app.route('/new_member_info', methods=['POST', 'GET'])   
def new_member_info():
    new_employee = mongo.db.employees
    new_employee.insert_one(request.form.to_dict())
    return render_template("new_member_info.html", new_first_name = new_first_name)    

if __name__ == '__main__':
    app.secret_key='1234'
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)