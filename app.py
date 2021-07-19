from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler  # this standard not required bcoz we are using tree randomforest algo (not imacting standard values)

app = Flask(__name__)

# Loading dump pickle ML model file
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))


@app.route('/')
def Home():
    return render_template('home.html')


@app.route("/car_Sale_Predict" ,methods=['POST'])
def car_Sale_Predict():
    if request.method=='POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['present_price'])
        Kms_Driven =int(request.form['Kms_Driven'])
        Fuel_Type = request.form['Fuel_Type']
        if Fuel_Type =='Petrol':
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif Fuel_Type =='Diesel':
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0

        Owner = int(request.form['Owner'])
        Seller_Type = request.form['Seller_Type']
        if Seller_Type=='Individual':
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
            
        Transmission = request.form['Transmission']
        if Transmission=='Mannual':
            Transmission_Manual=1
        else:
            Transmission_Manual=0

        Current_Year = 2021
        Total_car_Old= int(Current_Year-Year)

        Car_old_year=Total_car_Old

      # use our ML model to predict sell price using above data
        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Car_old_year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output=round(prediction[0],2)
    
        if output<0:
            return render_template('home.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('Result.html',Prediction_Result= output)

    else:
        return render_template('home.html')

if __name__=="__main__":
    #app.run(debug=True)
    #if we are aploading this on server then do below
    app.run(host='0.0.0.0', port=8080) # make sure AWS security grp have "Custom TCS = 8080 and access=anywhere"
    