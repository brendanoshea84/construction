import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
   

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone3"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')


mongo = PyMongo(app)

@app.route('/')
@app.route('/intro')
def intro():
    return render_template("intro.html", employees=mongo.db.employees.find_one())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)  