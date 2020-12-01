# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 00:38:25 2020

@author: Sayantan
"""

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import smtplib
from smtplib import SMTPException


app = Flask(__name__)
model = pickle.load(open('spam_model.pkl', 'rb'))
countvec = pickle.load(open('countvec.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    subject =  request.form["subject"]
    body =  request.form["body"]
    subject = "Subject: " + subject
    
    final_features = countvec.transform([subject +" "+ body])
    
    
    
    prediction = model.predict(final_features.todense())
    
    if prediction == 1:
        output = 'SPAM'
    else:
        output = 'NOT SPAM, Mail sent'
    
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        sender = 'harveysuit378@gmail.com'
        receiver = request.form["to"]
        
        #message = subject + " " + body
        
        message = '\r\n'.join(['To: %s' % receiver,
            'From: %s' % sender,
            'Subject: %s' % subject,
            '', body])
        
        
        server.login(sender, 'bond00711')
        server.sendmail(sender, receiver, message)
        
        server.quit()
        

    return render_template('index.html', prediction_text='Your mail is a {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
