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
    if request.method == 'POST':
        welcome_password = mongo.db.welcome_password.find()
        
        if welcome_password == request.form.get('new_password'): 
            return redirect(url_for('base'))
        
    return render_template('intro.html', employees=mongo.db.employees.find(), welcomes=mongo.db.welcome_password.find())       








@app.route('/base')
def base():
    print: "welcome"
    return render_template("base.html")






@app.route('/new_member_info')   
def new_member_info():
    print: "testing"
    return render_template("new_member_info.html")    

if __name__ == '__main__':
    app.secret_key='1234'
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)  