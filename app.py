import os
from flask import Flask, render_template, redirect, request, url_for, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 



app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone3"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')


mongo = PyMongo(app)

@app.route('/')
@app.route('/intro', methods=['POST', 'GET'])
def intro():
    if request.method == 'POST':
        welcome_password = mongo.db.welcome_password
        try_password = form.getvalue('new_password')

        if welcome_password == try_password:
            return render_template('new_member_info.html')


    return render_template("intro.html", employees=mongo.db.employees.find())  





@app.route('/new_member_info', methods=['POST', 'GET'])   
def new_member_info():
    return render_template("new_member_info.html")    

if __name__ == '__main__':
    app.secret_key='1234'
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)  