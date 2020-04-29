from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import os
import bcrypt
import calendar
import datetime
import itertools
from flask import Flask, render_template, redirect, request, url_for, session, flash


if os.path.exists("env.py"):
    import env

app = Flask(__name__, template_folder='templates')
app.config["MONGO_DBNAME"] = "milestone3"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
mongo = PyMongo(app)


@app.route('/intro', methods=['POST', 'GET'])
def intro():
    return render_template('intro.html')


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    employees = mongo.db.employees

    if request.method == 'POST':
        # Login using your own password
        login_user = employees.find_one(
            {'username': request.form.get('login')})

        # Check login passwords from input and collection
        if login_user:
            if bcrypt.hashpw(request.form.get('password_user').encode('utf-8'),
                             login_user['password']) == login_user['password']:
                global session
                session = login_user
                print(session)
                return redirect(url_for('home'))
            else:
                # Error flash
                flash('Wrong Password', 'login')

        else:
            flash('Username is incorrect', 'login')
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
            return redirect(url_for('add_personal_info'))
        else:
            flash('Wrong Password! Please contact Admin', 'sign_in')
    return render_template('intro.html', login=login)


@app.route('/new_member_info', methods=['POST', 'GET'])
def new_member_info():
    return render_template("/test/personal_info.html")


@app.route('/add_personal_info', methods=['POST', 'GET'])
def add_personal_info():
    employees = mongo.db.employees
    # Creating username number and username for new employee

    def add_to_database():
        post_data['first_name'] = request.form['first_name'].lower()
        post_data['last_name'] = request.form['last_name'].lower()
        post_data['password'] = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        new_id = employees.insert_one(post_data)
        global new_doc_id
        new_doc_id = new_id.inserted_id
        session = new_id

# When form is sent
    if request.method == 'POST':
        post_data = request.form.to_dict()
        # Create username
        # Insure input from form is lowercase
        temp_username = request.form['first_name'].lower(
        ) + '.' + request.form['last_name'].lower()

        # Check to see if username has been used
        temp_user = employees.find_one({'username': temp_username})

        if temp_user:
            # Create another username if username is been used before using dob
            tempdate = request.form['dob']
            testdate = tempdate.split('-')
            year = testdate[0]
            double_used_username = temp_username + year
            double_test = employees.find_one(
                {'username': double_used_username})

            if double_test:
                # If two usernames are the same, go to a page with suggestions
                return redirect(url_for('username_used'))
            else:
                # If double test name is free, make this the session
                post_data['username'] = double_used_username
                add_to_database()
                session = double_test

        else:
            post_data['username'] = temp_username
        # If test name is free, make this the session
            add_to_database()

        return redirect(url_for('emergcy'))
    return render_template("/employee_info/personal_info.html",
                           new_first_name=new_first_name)


@app.route('/bank_details', methods=['POST', 'GET'])
def bank_details():
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))

    if request.method == 'POST':
        # Update to made _id
        employees = mongo.db.employees
        employees.update_one({'_id': new_doc_id},
                             {'$set': {
                                 'bank_name': request.form.get('bank_name'),
                                 'bank_number': request.form.get('bank_number')
                             }}, upsert=True)
        return redirect(url_for('home'))
    return render_template("/employee_info/bank_details.html",
                           new_doc_id=new_doc_id,
                           username=username, new_first_name=new_first_name,
                           session=session)


@app.route('/emergcy', methods=['POST', 'GET'])
def emergcy():
    # Update to made _id
    global username
    employees = mongo.db.employees
    username = employees.find_one({'_id': new_doc_id})
    global session
    session = username
    for key, val in username.items():
        if 'username' in key:
            username = val

    if request.method == 'POST':
        employees.update_one({'_id': new_doc_id},
                             {'$set': {
                                 'next_of_kin': request.form.get('next_of_kin'),
                                 'next_of_kin_mob': request.form.get('next_of_kin_mob')
                             }}, upsert=True)
        return redirect(url_for('bank_details'))
    return render_template("/employee_info/emergcy.html",
                           new_doc_id=new_doc_id, username=username,
                           new_first_name=new_first_name, session=session)


@app.route('/add_project', methods=['POST', 'GET'])
def add_project():
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
        
    projects = mongo.db.projects

    if request.method == 'POST':
        post_data = request.form.to_dict()
        # Insure the price is an int not a string
        post_data['price'] = int(request.form['price'])
        # Set extra info for the project
        post_data['active'] = 'on'
        new_project_number = projects.distinct('project_number')
        project_no = max(new_project_number)
        project_number = int(project_no) + 1
        post_data['project_number'] = project_number
        projects.insert(post_data)
        # Back to projects
        return redirect(url_for('projects'))

    return render_template("/main_extras/edit_project.html", edit_project={},
                           session=session, projects=projects)


@app.route('/projects', methods=['POST', 'GET'])
def projects():
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
    projects = list(mongo.db.projects.find())
    return render_template("/main_extras/projects.html",
                           session=session, projects=projects)


@app.route('/edit_project/<project_id>', methods=['POST', 'GET'])
def edit_project(project_id):
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
    
    edit_project = mongo.db.projects.find_one({"_id": ObjectId(project_id)})

    if request.method == "POST":
        print("post happened")
        update_project = mongo.db.projects.update_one({"_id": ObjectId(project_id)},
                                                      {'$set': {
                                                          'name': request.form.get('name'),
                                                          'phone': request.form.get('phone'),
                                                          'address': request.form.get('address'),
                                                          'brief': request.form.get('brief'),
                                                          'discription': request.form.get('discription'),
                                                          'price': request.form.get('price'),
                                                          'price_type': request.form.get('price_type'),
                                                          'active': request.form.get('active')
                                                      }}, upsert=True)
        print("try after")
        return redirect(url_for('projects'))
    return render_template("/main_extras/edit_project.html", session=session,
                           edit_project=edit_project,
                           project=mongo.db.projects.find())


@app.route('/project_info/<project_id>', methods=['POST', 'GET'])
def project_info(project_id):
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
    project_info = mongo.db.projects.find_one({"_id": ObjectId(project_id)})
    return render_template("/main_extras/project_info.html",
                           session=session, project=project_info)


@app.route('/delete_project/<project_id>', methods=['POST', 'GET'])
def delete_project(project_id):
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
    delete_project = mongo.db.projects.remove({"_id": ObjectId(project_id)})
    return redirect(url_for('projects'))


@app.route('/employees', methods=['POST', 'GET'])
def employees():
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
    employees = mongo.db.employees.find()

    return render_template("/main_extras/employees.html",
                           session=session, employees=employees)


@app.route('/employee_info/<employee_id>', methods=['POST', 'GET'])
def employee_info(employee_id):
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
    
    employee_info = mongo.db.employees.find_one({"_id": ObjectId(employee_id)})
    return render_template("/main_extras/employee_info.html",
                           session=session, employee=employee_info)


@app.route('/edit_employee/<employee_id>', methods=['POST', 'GET'])
def edit_employee(employee_id):
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))

    edit_employee = mongo.db.employees.find_one({"_id": ObjectId(employee_id)})
    
    if request.method == "POST":
        print("post happened")
        update_employee = mongo.db.employees.update_one({"_id": ObjectId(employee_id)},
                                                        {'$set': {
                                                            'first_name': request.form.get('first_name'),
                                                            'last_name': request.form.get('last_name'),
                                                            'address': request.form.get('address'),
                                                            'dob': request.form.get('dob'),
                                                            'mob': request.form.get('mob'),
                                                            'home_number': request.form.get('home_number'),
                                                            'next_of_kin': request.form.get('next_of_kin'),
                                                            'next_of_kin_mob': request.form.get('next_of_kin_mob'),
                                                            'bank_name': request.form.get('bank_name'),
                                                            'bank_number': request.form.get('bank_number')
                                                        }}, upsert=True)
        return redirect(url_for('employees'))

    return render_template("/main_extras/edit_employee.html",
                           session=session, edit_employee=edit_employee)


@app.route('/time_log', methods=['POST', 'GET'])
def time_log():
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
    return render_template("/main_extras/timelogs.html")


@app.route('/time_log_new', methods=['POST', 'GET'])
def time_log_new():
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))

    post_data = request.form.to_dict()
    post_data['project_number'] = int(request.form['project_number'])
    post_data['date'] = request.form['date']
    post_data['hours'] = int(request.form['hours'])
    post_data['notes'] = request.form['notes']
    post_data['employee_id'] = session['username']
    mongo.db.time_logs.insert_one(post_data)
    return redirect(url_for('timelogs_info'))
    return render_template("/main_extras/timelogs.html", session=session)


@app.route('/timelogs_info', methods=['POST', 'GET'])
def timelogs_info():
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))

    # Get todays date/ week number / day name
    date_now = datetime.datetime.now()
    weekdays = date_now.strftime("%W")
    day = date_now.strftime("%A")

    # functions to change week
    week_day = date_now.isocalendar()[2]
    week_change = session.get('week_change', 0)

    if 'lastweek' in request.form:
        week_change += 1
        session['week_change'] = week_change
    elif 'nextweek' in request.form:
        week_change -= 1
        session['week_change'] = week_change
    else:
        print("not working")

    change_date = (week_change * 7)

    # Calculates Starting date (Monday)
    start_date = date_now - datetime.timedelta(days=week_day)

    # Prints the list of dates in a current week
    dates = list([str((start_date + datetime.timedelta(days=i+1 -
                                                       change_date)).date().strftime('%Y-%m-%d')) for i in range(7)])

    dates_org = list([str((start_date + datetime.timedelta(days=i +
                                                           1-change_date)).date().strftime('%d-%m')) for i in range(7)])

    day_names = list([str((start_date + datetime.timedelta(days=i +
                                                           1-change_date)).date().strftime('%a')) for i in range(7)])

    date_now = date_now.strftime('%Y-%m-%d')
    d = "2020-W" + weekdays
    # Monday as start of the week
    monday = datetime.datetime.strptime(
        d + '-1', "%Y-W%W-%w").strftime('%d-%m-%Y')
    employee = list(mongo.db.time_logs.find(
        {"employee_id": session['username']}))

    projects = list(mongo.db.projects.find())
    show_week = itertools.zip_longest(dates, day_names, dates_org)

    return render_template("/main_extras/timelogs_info.html", session=session,
                           worked={}, projects=projects, now=date_now,
                           weekdays=weekdays, day=day, dates=dates,
                           monday=monday, day_names=day_names,
                           employee=employee, show_week=show_week)


@app.route('/show_work/<worked_id>', methods=['POST', 'GET'])
def show_work(worked_id):
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))

    show_work = mongo.db.time_logs.find_one({"_id": ObjectId(worked_id)})

    # Get todays date/ week number / day name
    date_now = datetime.datetime.now()
    weekdays = date_now.strftime("%W")
    day = date_now.strftime("%A")

    # functions to change week
    week_day = date_now.isocalendar()[2]
    week_change = session.get('week_change', 0)

    if 'lastweek' in request.form:
        week_change += 1
        session['week_change'] = week_change
    elif 'nextweek' in request.form:
        week_change -= 1
        session['week_change'] = week_change
    else:
        print("not working")

    change_date = (week_change * 7)

    # Calculates Starting date (Monday)
    start_date = date_now - datetime.timedelta(days=week_day)

    # Prints the list of dates in a current week
    dates = list([str((start_date + datetime.timedelta(days=i+1 -
                                                       change_date)).date().strftime('%Y-%m-%d')) for i in range(7)])

    dates_org = list([str((start_date + datetime.timedelta(days=i +
                                                           1-change_date)).date().strftime('%d-%m')) for i in range(7)])

    day_names = list([str((start_date + datetime.timedelta(days=i +
                                                           1-change_date)).date().strftime('%a')) for i in range(7)])

    date_now = date_now.strftime('%Y-%m-%d')
    d = "2020-W" + weekdays
    # Monday as start of the week
    monday = datetime.datetime.strptime(
        d + '-1', "%Y-W%W-%w").strftime('%d-%m-%Y')
    employee = list(mongo.db.time_logs.find(
        {"employee_id": session['username']}))

    projects = list(mongo.db.projects.find())
    show_week = itertools.zip_longest(dates, day_names, dates_org)

    if request.method == "POST":
        print("post happened")
        update_show_work = mongo.db.show_work.update_one({"_id": ObjectId(worked_id)},
                                                         {'$set': {
                                                             'project_number': request.form.get('project_number'),
                                                             'date': request.form.get('date_timelog'),
                                                             'hours': request.form.get('hours'),
                                                             'notes': request.form.get('notes')
                                                         }}, upsert=True)
        return redirect(url_for('get_date'))

    return render_template("/main_extras/timelogs_info.html", session=session,
                           worked=show_work, projects=projects, now=date_now,
                           weekdays=weekdays, day=day, dates=dates,
                           monday=monday, day_names=day_names,
                           employee=employee, show_week=show_week)


@app.route('/delete_employee/<delete_id>', methods=['POST', 'GET'])
def delete_employee(delete_id):
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))

    delete_employee = mongo.db.employees.find_one({"_id": ObjectId(delete_id)})
    return render_template("/main_extras/delete.html",
                           session=session, employee=delete_employee)


@app.route('/remove_employee/<delete_id>', methods=['POST', 'GET'])
def remove_employee(delete_id):
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))

    delete_project = mongo.db.employees.remove({"_id": ObjectId(delete_id)})
    return redirect(url_for('employees'))


@app.route('/home', methods=['POST', 'GET'])
def home():
    # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))

    news = mongo.db.news.find()
    if request.method == "POST":
        post_data = request.form.to_dict()
        post_data['heading'] = request.form['title']
        post_data['news'] = request.form['news']
        mongo.db.news.insert_one(post_data)
        return redirect(url_for('home'))
    return render_template("/main_extras/home.html", news=news, session=session)


@app.route('/delete_new/<new_id>', methods=['POST', 'GET'])
def delete_new(new_id):
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))

    delete_new = mongo.db.news.remove({"_id": ObjectId(new_id)})
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/not_logged_in')
def not_logged_in():
    return render_template("/errors/not_logged_in.html")

@app.route('/username_used')
def username_used():
    return render_template("/errors/username_used.html")    

@app.route('/base', methods=['POST', 'GET'])
def base():
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
    return render_template("base.html")


@app.route('/main', methods=['POST', 'GET'])
def main():
        # Check if user is logged in
    if session.get('username') == None:
        return redirect(url_for('not_logged_in'))
    return render_template("main.html", session=session)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
