import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from tkinter import messagebox as mb

app = Flask(__name__)
app.secret_key='1234'
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
                return redirect(url_for('add_personal_info'))
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


@app.route('/new_member_info', methods=['POST', 'GET'])   
def new_member_info():
        
    return render_template("/employeeinfo/personal_info.html", employees=mongo.db.employees.find())    


@app.route('/add_personal_info', methods=['POST', 'GET'])
def add_personal_info():
    # Creating username number and username for new employee
    # New User employee number
    new_employee = mongo.db.employees
    # Find highest employee number
    employ_number = new_employee.distinct('employee_number')
    new_number = max(employ_number) 
    employee_number = int(new_number) +1
    session['login_user'] = employee_number

    print("testing area 1")

# When form is sent
    if request.method == 'POST': 
        if 'personal_info_btn' in request.form:
        
            post_data = request.form.to_dict()

        # Create username
        # Insure input from form is lowercase
            employee_first_name = request.form['employee_first_name'].lower()
            employee_last_name = request.form['employee_last_name'].lower()
            employee_username = (employee_first_name + '.' + employee_last_name)
        
            post_data['employee_username'] = employee_username
            post_data['employee_number'] = employee_number
            post_data['employee_first_name'] = employee_first_name
            post_data['employee_last_name'] = employee_last_name
            print("tesing sending")
             
            # Get the id of the new insert to collections 
            new_id = new_employee.insert_one(post_data)
            global new_doc_id
            new_doc_id = new_id.inserted_id
        return redirect(url_for('emergcy'))
    return render_template("/employeeinfo/personal_info.html", employees=mongo.db.employees.find(), new_first_name=new_first_name)     


@app.route('/qualifications', methods=['POST', 'GET'])
def qualifications():
    return render_template("/employeeinfo/emergcy.html")


@app.route('/personal_info', methods=['POST', 'GET'])
def personal_info():
    return render_template("")

@app.route('/bank_details', methods=['POST', 'GET'])
def bank_details():
    return render_template("/employeeinfo/bank_details.html")




@app.route('/emergcy/', methods=['POST', 'GET'])
def emergcy():
    if request.method == 'POST':
        this_user = mongo.db.employees
        this_user.update_one({'_id': new_doc_id},
        {'$set': {
        'employee_next_of_keen': request.form.get('employee_next_of_keen'),
        'employee_next_of_keen_mob': request.form.get('employee_next_of_keen_mob')
        }}, upsert= True)
        return redirect(url_for('qualifications'))
    return render_template("/employeeinfo/emergcy.html", new_doc_id=new_doc_id)    





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




# Log out
@app.route("/logout")  
def logout(): 
    session.pop("user", None) 
    return redirect(url_for("/intro"))

if __name__ == '__main__':
    
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)