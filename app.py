import os, bcrypt, calendar, datetime, itertools
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.secret_key = '1234'
app.config["MONGO_DBNAME"] = "milestone3"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# Welcome Page
# Sign in for new members with a pre password
# Login using your own password


@app.route('/intro', methods = ['POST', 'GET'])
def intro():
    return render_template ('intro.html', employee = mongo.db.employees)      


@app.route('/', methods=['POST', 'GET'])
@app.route('/sign_in', methods=['POST','GET'])
def sign_in():
    # set employees to global variable
    global employees
    employees = mongo.db.employees

    if request.method == 'POST':
        # Login using your own password
        login_user = employees.find_one({'username': request.form.get('login')})

        if login_user:
            if bcrypt.hashpw(request.form.get('password_user').encode('utf-8'), login_user['password']) == login_user['password']:
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
        session = new_id
   
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
    global session
    session = username
    print("testing sessions ")
    print(session)
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
        post_data['active'] = 'on'

        new_project_number = projects.distinct('project_number')
        project_no = max(new_project_number) 
        project_number = int(project_no) +1
        post_data['project_number'] = project_number

        print("testing 189")
        
        print (project_number)

        projects.insert_one(post_data)
        return redirect(url_for('projects'))


    return render_template("/main_extras/projects_new.html", session=session, projects=projects)

@app.route('/projects', methods=['POST', 'GET'])
def projects():
    return render_template("/main_extras/projects.html", session=session, projects = mongo.db.projects.find(), closes = mongo.db.projects.find())

@app.route('/edit_projects/<project_id>', methods=['POST', 'GET'])
def edit_projects(project_id):
    print("edit 209")
    edit_projects = mongo.db.projects.find_one({"_id":ObjectId(project_id)})

    if request.method == "POST":
        print("post happened")
        update_project = mongo.db.projects.update_one({"_id":ObjectId(project_id)},
        {'$set': {
            
            'name':request.form.get('name'),
            'phone':request.form.get('phone'),
            'address':request.form.get('address'),
            'brief':request.form.get('brief'),
            'discription':request.form.get('discription'),
            'price':request.form.get('price'),
            'price_type':request.form.get('price_type'),
            'active':request.form.get('active')

        }}, upsert= True)
        print("try after")
        return redirect(url_for('projects'))
    return render_template("/main_extras/edit_projects.html", session=session, edit_projects = edit_projects ,project = mongo.db.projects.find())

@app.route('/get_projects/<project_id>', methods=['POST', 'GET'])
def get_projects(project_id):
    get_project = mongo.db.projects.find_one({"_id":ObjectId(project_id)})
    return render_template("/main_extras/get_projects.html", session=session, project = get_project)

@app.route('/delete_projects/<project_id>', methods=['POST', 'GET'])
def delete_projects(project_id):
    delete_project = mongo.db.projects.remove({"_id":ObjectId(project_id)})
    return redirect(url_for('projects'))


@app.route('/employees', methods=['POST', 'GET'])
def employees():
    print ("going to employees")
    return render_template("/main_extras/employees.html", session=session, employees = mongo.db.employees.find())
    
@app.route('/get_employee/<employee_id>', methods=['POST', 'GET'])
def get_employee(employee_id):
    print ("going to employees")
    get_employee = mongo.db.employees.find_one({"_id":ObjectId(employee_id)})
    return render_template("/main_extras/get_employee.html", session=session, employee = get_employee)
    


@app.route('/edit_employee/<employee_id>', methods=['POST', 'GET'])
def edit_employee(employee_id):
    edit_employee = mongo.db.employees.find_one({"_id":ObjectId(employee_id)})
    print ("going to employees")

    if request.method == "POST":
        print("post happened")
        update_employee = mongo.db.employees.update_one({"_id":ObjectId(employee_id)},
        {'$set': {
            
            'first_name':request.form.get('first_name'),
            'last_name':request.form.get('last_name'),
            'address':request.form.get('address'),
            'dob':request.form.get('dob'),
            'mob':request.form.get('mob'),
            'home_number':request.form.get('home_number'),
            'next_of_kin':request.form.get('next_of_kin'),
            'next_of_kin_mob':request.form.get('next_of_kin_mob'),
            'bank_name':request.form.get('bank_name'),
            'bank_number':request.form.get('bank_number')


        }}, upsert= True)
        return redirect(url_for('employees'))

    return render_template("/main_extras/edit_employee.html", session = session, edit_employee = edit_employee)
    





@app.route('/time_log', methods=['POST', 'GET'])
def time_log():
    print ("going to time_log")
    x = datetime.datetime.now()
    weekdays = x.strftime("%W")
    day = x.strftime("%A")

    week_day=datetime.datetime.now().isocalendar()[2]
     
    week_change = session.get('week_change', 0)
    
    if 'lastweek' in request.form:
        week_change += 1
        session['week_change'] = week_change
        print("last week changed")
        print(week_change)
    elif 'nextweek' in request.form:
        week_change -= 1
        session['week_change'] = week_change
        print("next week changed") 
        print(week_change)  
    else:
        print("not working")     

    change_date = (week_change * 7)

    # Calculates Starting date (Monday) for this case by subtracting current date with time delta of the day of the week
    start_date = x - datetime.timedelta(days=week_day)

    # Prints the list of dates in a current week
    dates = list([str((start_date + datetime.timedelta(days=i+1-change_date)).date().strftime('%m-%d')) for i in range(7)])
    day_names = list([str((start_date + datetime.timedelta(days=i+1-change_date)).date().strftime('%a')) for i in range(7)])
    
    d = "2020-W" + weekdays

    r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w").strftime('%m-%d')
    testingABC = list(mongo.db.time_logs.find())

    qqq = list(mongo.db.time_logs.find())
    

    
    return render_template("/main_extras/timelogs.html", session=session, time=x, weekdays=weekdays, day=day, dates=dates, r=r, day_names=day_names,projects = mongo.db.projects.find(), testingABC= testingABC, testing = itertools.zip_longest(dates, day_names, testingABC), qqq=qqq )
    





@app.route('/delete_employee/<delete_id>', methods=['POST', 'GET'])
def delete_employee(delete_id):
    delete_employee = mongo.db.employees.find_one({"_id":ObjectId(delete_id)})
    return render_template("/main_extras/delete.html", session=session, employee = delete_employee)
  
@app.route('/remove_employee/<delete_id>', methods=['POST', 'GET'])
def remove_employee(delete_id):
    delete_project = mongo.db.employees.remove({"_id":ObjectId(delete_id)})
    return redirect(url_for('employees'))






    

@app.route('/base', methods=['POST', 'GET'])
def messages():
    print ("working at messages")
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