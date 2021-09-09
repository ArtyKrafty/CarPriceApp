from flask import Flask,request, url_for, redirect, render_template, jsonify
from pycaret.regression import *
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

model = load_model('deployment_05092021')
cols = ['RegistrationYear', 'Gearbox', 'Power', 'Kilometer', 'FuelType', 'Brand']

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict',methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    final = np.array(int_features)
    data_unseen = pd.DataFrame([final], columns = cols)
    prediction = predict_model(model, data=data_unseen, round = 0)
    prediction = int(prediction.Label[0])
    temp_1 = render_template('home.html',pred_1=f'Expected Price for {final[5]} of {final[0]} year, with {final[1]} kW, {final[2]} miles run, {final[3]} gearbox, {final[4]} fuel type will be')
    temp_2 = render_template('home.html',pred_2=f'{prediction} $')
    return temp_1, temp_2

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = predict_model(model, data=data_unseen)
    output = prediction.Label[0]
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
