from flask import Flask, request
import pandas as pd
import numpy as np
import pickle
from sklearn import preprocessing
import flasgger
from flasgger import Swagger
import requests
from sklearn.preprocessing import MinMaxScaler
import streamlit as st

#app = Flask(__name__)
#Swagger(app)

pickle_in=open('telecom_model.pkl', 'rb')
model = pickle.load(pickle_in)

#@app.route('/')
def welcome():
    return "Telecom Churn prediction model"

#@app.route("/predict", methods=['POST'])
def prediction(tenure, PhoneService, PaperlessBilling, MonthlyCharges, TotalCharges, SeniorCitizen, Partner, Dependents, Contract_One_year, Contract_Two_year, PaymentMethod_Credit_card_automatic, PaymentMethod_Electronic_check, PaymentMethod_Mailed_check, InternetService_Fiber_optic, InternetService_No, OnlineSecurity_Yes, OnlineBackup_Yes, DeviceProtection_Yes, TechSupport_Yes):

    """
    ---
    parameters:
        - name: tenure
          in: query
          type: number
          description: "Enter the tenure of service minimum 0 and maximum 72"
          required: true
        - name: PhoneService
          in: query
          enum: [
          "Yes",
          "No"
          ]
          type: string
          required: true
        - name: PaperlessBilling
          in: query
          type: string
          enum: [
          "Yes",
          "No"
          ]
          required: true
        - name: MonthlyCharges
          in: query
          type: number
          required: true
        - name: TotalCharges
          in: query
          type: number
          required: true
        - name: SeniorCitizen
          in: query
          type: string
          enum: [
          "Yes",
          "No"
          ]
          required: true
        - name: Partner
          in: query
          type: string
          required: true
          enum: [
          "Yes",
          "No"
          ]
        - name: Dependents
          in: query
          type: string
          enum: [
          "Yes",
          "No"
          ]
          required: true
        - name: Contract
          in: query
          type: string
          enum: [
          "One Month",
          "One Year",
          "Two Year"
          ]
          required: true
        - name: PaymentMethod
          in: query
          type: string
          enum: [
          "Credit Card",
          "Bank Transfer",
          "Electronic check",
          "Mailed check"
          ]
          required: true
        - name: InternetService
          in: query
          type: string
          enum: [
          "DSL",
          "Fiber Optic",
          "No Internet service"
          ]
          required: true
        - name: OnlineSecurity
          in: query
          type: string
          enum: [
          "Yes",
          "No"
          ]
          required: true
        - name: OnlineBackup
          in: query
          type: string
          enum: [
          "Yes",
          "No"
          ]
          required: true
        - name: DeviceProtection
          in: query
          type: string
          enum: [
          "Yes",
          "No"
          ]
          required: true
        - name: TechSupport
          in: query
          type: string
          enum: [
          "Yes",
          "No"
          ]
          required: true
    responses:
        200:
            description: The output values
    """
    col_names = ['tenure', 'PhoneService', 'PaperlessBilling', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen', 'Partner', 'Dependents', 'Contract_One year', 'Contract_Two year', 'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check', 'InternetService_Fiber optic', 'InternetService_No', 'OnlineSecurity_Yes', 'OnlineBackup_Yes', 'DeviceProtection_Yes', 'TechSupport_Yes']
    X_values = pd.DataFrame([tenure, PhoneService, PaperlessBilling, MonthlyCharges, TotalCharges, SeniorCitizen, Partner, Dependents, Contract_One_year, Contract_Two_year, PaymentMethod_Credit_card_automatic, PaymentMethod_Electronic_check, PaymentMethod_Mailed_check, InternetService_Fiber_optic, InternetService_No, OnlineSecurity_Yes, OnlineBackup_Yes, DeviceProtection_Yes, TechSupport_Yes], index=col_names).T
    X_values = X_values.apply(pd.to_numeric)
    prediction = model.predict(X_values)
    if str(prediction) == '[1]':
        return "The customer will churn"
    elif str(prediction) == '[0]':
        return "The customer will stay"

def main():
    st.title("Telecom Churn prediction Model")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit Telecom Churn prediction ML App </h2>
    </div>
    """
    Contract_One_year = 0
    Contract_Two_year = 0
    PaymentMethod_Credit_card_automatic = 0
    PaymentMethod_Electronic_check = 0
    PaymentMethod_Mailed_check = 0
    InternetService_Fiber_optic = 0
    InternetService_No = 0
    OnlineSecurity_Yes = 0
    OnlineBackup_Yes = 0
    DeviceProtection_Yes = 0
    TechSupport_Yes = 0
    tenure = st.text_input("Tenure", "Type Here")
    PhoneService = st.selectbox('Is the customer using Phone service?',('Yes', 'No'))
    if PhoneService == 'Yes':
        PhoneService = 1
    else:
        PhoneService = 0
    PaperlessBilling = st.selectbox("Is the customer using Paperless Billing?", ('Yes', 'No'))
    if PaperlessBilling == 'Yes':
        PaperlessBilling = 1
    else:
        PaperlessBilling = 0  
    MonthlyCharges = st.text_input("MonthlyCharges", "Type the monthly charge here")
    TotalCharges = st.text_input("TotalCharges", "Type the total charge here")
    SeniorCitizen = st.selectbox("Is the customer a senior citizen?", ('Yes', 'No'))
    if SeniorCitizen == 'Yes':
        SeniorCitizen = 1
    else:
        SeniorCitizen = 0 
    Partner = st.selectbox('Does the customer has a partner?', ('Yes', 'No'))    
    if Partner == 'Yes':
        Partner = 1
    else:
        Partner = 0 
    Dependents = st.selectbox('Does the customer has any dependants?', ('Yes', 'No'))
    if Dependents == 'Yes':
        Dependents = 1
    else:
        Dependents = 0 
    Contract = st.selectbox('Select the customer contract period', ('One Month', 'One Year', 'Two Year'))
    if Contract == 'One Month':
        Contract_One_year = 0
        Contract_Two_year = 0
    elif Contract == 'One Year':
        Contract_One_year = 1
        Contract_Two_year = 0
    else:
        Contract_One_year = 0
        Contract_Two_year = 1 
    PaymentMethod = st.selectbox('Select the customer Payment method', ('Credit Card', 'Bank Transfer', 'Electronic Check', 'Mailed Check'))
    if PaymentMethod == 'Credit Card':
        PaymentMethod_Credit_card_automatic = 1
        PaymentMethod_Electronic_check = 0
        PaymentMethod_Mailed_check = 0
    elif PaymentMethod == 'Electronic Check':
        PaymentMethod_Credit_card_automatic = 0
        PaymentMethod_Electronic_check = 1
        PaymentMethod_Mailed_check = 0    
    elif PaymentMethod == 'Mailed Check':
        PaymentMethod_Credit_card_automatic = 0
        PaymentMethod_Electronic_check = 0
        PaymentMethod_Mailed_check = 1
    InternetService = st.selectbox('What kind of internet service the customer has subscribed?', ('DSL', 'Fiber Optic', 'No internet'))
    if InternetService == 'Fiber Optic':
        InternetService_Fiber_optic = 1
        InternetService_No = 0
    elif InternetService == 'No internet':
        InternetService_Fiber_optic = 0
        InternetService_No = 1  
    OnlineSecurity = st.selectbox('Is the customer using online security?', ('Yes', 'No'))
    if OnlineSecurity == 'Yes':
        OnlineSecurity_Yes = 1
    else:
        OnlineSecurity_Yes = 0
    OnlineBackup = st.selectbox('Is the customer using online backup?', ('Yes', 'No'))
    if OnlineBackup == 'Yes':
        OnlineBackup_Yes = 1
    else:
        OnlineBackup_Yes = 0
    DeviceProtection = st.selectbox('Is the customer using device protection?', ('Yes', 'No'))
    if DeviceProtection == 'Yes':
        DeviceProtection_Yes = 1
    else:
        DeviceProtection_Yes = 0
    TechSupport = st.selectbox('Is the customer using tech support?', ('Yes', 'No'))
    if TechSupport == 'Yes':
        TechSupport_Yes = 1
    else:
        TechSupport_Yes = 0
    result=""
    if st.button("Predict"):
        result = prediction(tenure, PhoneService, PaperlessBilling, MonthlyCharges, TotalCharges, SeniorCitizen, Partner, Dependents, Contract_One_year, Contract_Two_year, PaymentMethod_Credit_card_automatic, PaymentMethod_Electronic_check, PaymentMethod_Mailed_check, InternetService_Fiber_optic, InternetService_No, OnlineSecurity_Yes, OnlineBackup_Yes, DeviceProtection_Yes, TechSupport_Yes)
    st.success(result)

if __name__ == '__main__':
    main()