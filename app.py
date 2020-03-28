import os
import bcrypt
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.secret_key='1234'
app.config["MONGO_DBNAME"] = "milestone3"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# Welcome Page
# Sign in for new members with a pre password
# Login using your own password

@app.route('/intro', methods=['POST', 'GET'])     
def intro():            
    return render_template('intro.html', employee = mongo.db.employees)      

@app.route('/', methods=['POST', 'GET'])
@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
    # Login using your own password
        print("after post")
        employees = mongo.db.employees
        login_user =  employees.find_one({'username' : request.form.get('login')})
        
        print("before test")
        if login_user:
            if bcrypt.hashpw(request.form.get('password_user').encode('utf-8'), login_user['password']) ==  login_user['password']:
                print("testing login area")
                session['username'] = request.form['username']
                
                return redirect(url_for('main'))
            else:
                # Fix here
                # Add error msg
                print("error at login")
    return render_template('intro.html', employee = mongo.db.employees)       
            
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST': 
    # Sign in for new members with a pre password
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
            # Fix here
            # flash("testing")
            print("welcome password wrong")
    return render_template('intro.html')       


@app.route('/new_member_info', methods=['POST', 'GET'])   
def new_member_info():
       
    return render_template("/employeeinfo/personal_info.html")    

@app.route('/add_personal_info', methods=['POST', 'GET'])
def add_personal_info():
    # Creating username number and username for new employee
    new_employee = mongo.db.employees
   
# When form is sent
    if request.method == 'POST': 
        post_data = request.form.to_dict()
        # Create username
        # Insure input from form is lowercase  
        temp_username = request.form['first_name'].lower() + '.' + request.form['last_name'].lower()
        
        # Check to see if username has been used
        temp_user = new_employee.find_one({'username' : temp_username})

        if temp_user:
            # Create another username if username is been used before using dob
            print("already in database")
            tempdate = request.form['dob']
            testdate = tempdate.split('-')
            year = testdate[0]
            double_used_username = request.form['first_name'].lower() + '.' + request.form['last_name'].lower() + year
            double_test = new_employee.find_one({'username' : double_used_username})

            if double_test:
                # If two usernames are the same, go to a page with suggestions
                return redirect(url_for('username_wrong'))
                post_data['username'] = request.form['first_name'].lower() + '.' + request.form['last_name'].lower() + year
        else:
            post_data['username'] = temp_username

        post_data['first_name'] = request.form['first_name'].lower()
        post_data['last_name'] = request.form['last_name'].lower() 
        post_data['password'] = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Get the id of the new insert to collections 
        new_id = new_employee.insert_one(post_data)
        global new_doc_id

        # insert to collections
        new_doc_id = new_id.inserted_id
        return redirect(url_for('emergcy'))
    return render_template("/employeeinfo/personal_info.html", new_first_name=new_first_name)     


@app.route('/bank_details', methods=['POST', 'GET'])
def bank_details():
    if request.method == 'POST':
        # Update to made _id 
        this_user.update_one({'_id': new_doc_id},
        {'$set': {
        'bank_name': request.form.get('bank_name'),
        'bank_number': request.form.get('bank_number')
        }}, upsert= True)
        return redirect(url_for('main'))
    return render_template("/employeeinfo/bank_details.html", this_user=this_user, new_doc_id=new_doc_id, username =username, new_first_name=new_first_name)

@app.route('/emergcy/', methods=['POST', 'GET'])
def emergcy():
    global this_user
    global username
    this_user = mongo.db.employees
    username = this_user.find_one({'_id': new_doc_id})
    for key, val in username.items():
        if 'username' in key:
            username = val
    print(username)
    if request.method == 'POST':
        this_user.update_one({'_id': new_doc_id},
        {'$set': {
        'next_of_kin': request.form.get('next_of_kin'),
        'next_of_kin_mob': request.form.get('next_of_kin_mob')
        }}, upsert= True)
        return redirect(url_for('bank_details'))
    return render_template("/employeeinfo/emergcy.html", new_doc_id=new_doc_id, username =username, new_first_name=new_first_name)    



@app.route('/personal_info', methods=['POST', 'GET'])
def personal_info():
    return render_template("")

@app.route('/main', methods=['GET'])
def main():
    print ("going to main")
    
    return render_template("main.html")

@app.route('/base', methods=['POST', 'GET'])
def base():
    print ("working at base")
    return render_template("base.html")

@app.route('/error_existing')
def error_existing():
    return render_template("error_existing.html")




# If username has been used twice before and this is the third time
@app.route('/username_wrong')
def username_wrong():
    print("too many users, not enough names")
    return render_template("error_existing.html")    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)