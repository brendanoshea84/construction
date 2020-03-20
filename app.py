import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone3"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route('/', methods=['POST', 'GET'])
@app.route('/intro', methods=['POST', 'GET'])
def new_member():
    

    if request.method == 'GET':
        print ("GET working")
        
        
    if request.method == 'POST':
        try_pass = request.form.get('new_password')
        w_password = mongo.db.welcome_password.find_one()
        for key, val in w_password.items():
            if 'welcome_password' in key:
                wel_pass = val
        print (wel_pass)
        print ("POST working")
        print ("test 2") 
        print (try_pass)
    
        if wel_pass == try_pass:
            
            print ("try and pass") 
            print (w_password == try_pass)
            return redirect(url_for('new_member_info'))
        
    return render_template('intro.html', employees=mongo.db.employees.find(), welcomes=mongo.db.welcome_password.find())       








@app.route('/base')
def base():
    
    return render_template("base.html")






@app.route('/new_member_info', methods=['POST', 'GET'])   
def new_member_info():
    if request.method == 'POST':
        print ("POST working in wrong spot")
    print ("TESTING ABC")
    return render_template("new_member_info.html")    

if __name__ == '__main__':
    app.secret_key='1234'
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)  