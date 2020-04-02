import os, bcrypt
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
    # set employees to global variable
    global employees
    employees = mongo.db.employees
    print(employees)

    if request.method == 'POST':
    # Login using your own password
        login_user =  employees.find_one({'username' : request.form.get('login')})
        
        if login_user:
            if bcrypt.hashpw(request.form.get('password_user').encode('utf-8'), login_user['password']) ==  login_user['password']:
                global session
                session = login_user
                print(session)
                print("testing problem area 38")
                return redirect(url_for('main'))
            else:
                # Fix here
                # Add error msg
                print("error at login 40")
        else:
            print("no user 42")        
    return render_template('intro.html')       
            
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
            print("success with password at sign_up: line 59")
            return redirect(url_for('add_personal_info'))
        else:
            # Fix here
            # flash("testing")
            print("welcome password wrong line 64")
    return render_template('intro.html')       


@app.route('/new_member_info', methods=['POST', 'GET'])   
def new_member_info():
       
    return render_template("/employeeinfo/personal_info.html")    

@app.route('/add_personal_info', methods=['POST', 'GET'])
def add_personal_info():
    # Creating username number and username for new employee
    
    def add_to_database():
        post_data['first_name'] = request.form['first_name'].lower()
        post_data['last_name'] = request.form['last_name'].lower() 
        post_data['password'] = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        new_id = employees.insert_one(post_data)
        global new_doc_id
        new_doc_id = new_id.inserted_id
   
# When form is sent
    if request.method == 'POST': 
        post_data = request.form.to_dict()
        # Create username
        # Insure input from form is lowercase  
        temp_username = request.form['first_name'].lower() + '.' + request.form['last_name'].lower()
        
        # Check to see if username has been used
        temp_user = employees.find_one({'username' : temp_username})

        if temp_user:
            # Create another username if username is been used before using dob
            print("already in database line 97")
            tempdate = request.form['dob']
            testdate = tempdate.split('-')
            year = testdate[0]
            double_used_username = temp_username + year
            double_test = employees.find_one({'username' : double_used_username})

            if double_test:
                # If two usernames are the same, go to a page with suggestions
                print("double test fail line 106")
                return redirect(url_for('username_wrong'))
            else:
                # If double test name is free, make this the session
                post_data['username'] = double_used_username
                add_to_database()
                session = double_test
                print("session loggin double 113")
                print(session)
                print("from 115")

        else:
            post_data['username'] = temp_username
        # If test name is free, make this the session
            add_to_database()
            session = temp_user
            print(session)
            print("session 123")

        return redirect(url_for('emergcy'))
    return render_template("/employeeinfo/personal_info.html", new_first_name=new_first_name)     


@app.route('/bank_details', methods=['POST', 'GET'])
def bank_details():
    if request.method == 'POST':
        # Update to made _id 
        employees.update_one({'_id': new_doc_id},
        {'$set': {
        'bank_name': request.form.get('bank_name'),
        'bank_number': request.form.get('bank_number')
        }}, upsert= True)
        return redirect(url_for('projects'))
    return render_template("/employeeinfo/bank_details.html", new_doc_id=new_doc_id, username =username, new_first_name=new_first_name)

@app.route('/emergcy/', methods=['POST', 'GET'])
def emergcy():
    global username
    username = employees.find_one({'_id': new_doc_id})
    for key, val in username.items():
        if 'username' in key:
            username = val
    print(username)
    print('username: line 150')
    if request.method == 'POST':
        employees.update_one({'_id': new_doc_id},
        {'$set': {
        'next_of_kin': request.form.get('next_of_kin'),
        'next_of_kin_mob': request.form.get('next_of_kin_mob')
        }}, upsert= True)
        return redirect(url_for('bank_details'))
    return render_template("/employeeinfo/emergcy.html", new_doc_id=new_doc_id, username =username, new_first_name=new_first_name)    



@app.route('/personal_info', methods=['POST', 'GET'])
def personal_info():
    return render_template("")

@app.route('/main', methods=['POST', 'GET'])
def main():
    print ("going to main")
    print(session)
    return render_template("main.html", session=session)


@app.route('/add_projects', methods=['POST', 'GET'])
def add_project():
    global projects
    projects = mongo.db.projects

    if request.method == 'POST': 
        post_data = request.form.to_dict()
        # Insure the price is an int not a string
        post_data['price'] = int(request.form['price'])
        # Set extra info for the project
        post_data['active'] = True

        new_project_number = projects.distinct('project_number')
        project_no = max(new_project_number) 
        project_number = int(project_no) +1
        post_data['project_number'] = project_number

        print("testing 189")
        
        print (project_number)

        projects.insert_one(post_data)

    return render_template("/main_extras/projects_new.html", session=session)

@app.route('/projects', methods=['POST', 'GET'])
def projects():
    return render_template("/main_extras/projects.html", session=session)


@app.route('/base', methods=['POST', 'GET'])
def base():
    print ("working at base")
    return render_template("base.html")

@app.route('/error_existing')
def error_existing():
    return render_template("/errors/error_existing.html")




# If username has been used twice before and this is the third time
@app.route('/username_wrong')
def username_wrong():
    print("too many users, not enough names")
    return render_template("error_existing.html")    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)