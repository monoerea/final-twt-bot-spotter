'''libraries used
pip install Flask
pip install joblib


Deploying machine learning models as web services.
The simplest way to deploy a machine learning model is to create a web service for prediction. 
In this example, we use the Flask web framework.
'''

from flask import Flask,request,jsonify,render_template
import joblib
import pandas as pd
import numpy as np
import pickle
import json
from model import getUserFlask as getUser
from model import getStatusFlask as getStatus
testvariable=0

# Create flask app
flask_app = Flask(__name__)
classifier = joblib.load('data/classifier_statusInfo.pkl')

@flask_app.route("/")
def Home():
    return render_template("index.html")
@flask_app.route("/predict", methods = ["POST"])
def predict():
    with open('data/json/oneuser.json', 'r') as data_file:
        userList = data_file.read()
    users = getUser.getUser(userList) #getting users
    status = getStatus.getStatus(userList,2) #getting status NEVER LESS THAN 2 
    print(users)
    print(type(users))

    prediction = classifier.predict(status)
    return render_template("index.html", result_here = prediction)
if __name__ == "__main__":
    flask_app.run(debug=True, host='0.0.0.0',port=8080)