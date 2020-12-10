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
from nltk import word_tokenize
import pandas


app = Flask(__name__)
model = pickle.load(open('spam_model.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))
final_df_columns = pickle.load(open('final_df.columns.pkl', 'rb'))
feat_imp = pandas.Series(model.feature_importances_, index=final_df_columns)


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
    subject = subject
    
    
    tfidf_features = tfidf.transform([subject +" "+ body])
    
    
    tfidf_vect = tfidf_features.todense()
    
    #final_features = np.hstack((count_vect, tfidf_vect))
    final_features = tfidf_vect
    prediction = model.predict(final_features)
    score = model.predict_proba(final_features)[0]
    
    #print(feat_imp['money'])
    if prediction == 1:
        output = 'a SPAM'
        tokens = word_tokenize(subject +" "+ body)
        
        importance = []
        for i in tokens:
            try:
                sc = feat_imp[str(i).lower()]
                importance.append([sc, i])
                
            except:
                pass
            
            

    
        importance.sort(reverse=True)
        results = []
        count = 0
        for i in importance:
            results.append(i)
            count +=1
            if count>10:
                break
            
            
    else:
        output = 'NOT a SPAM, Mail sent!'
        
        tokens = word_tokenize(subject +" "+ body)
        print(tokens)
        importance = []
        
        for i in tokens:
            try:
                sc = feat_imp[str(i).lower()]
                importance.append([sc, i])
            except:
                pass
        print(importance)
        importance.sort()
        results = []
        count = 0
        for i in importance:
            results.append(i)
            count +=1
            if count>10:
                break
        
    
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
        

    return render_template('index.html', prediction_text='Your mail is {}'.format(output), spam_score = str(score[1]), non_spam_score = str(score[0]), results = results)


if __name__ == "__main__":
    app.run(debug=True)
