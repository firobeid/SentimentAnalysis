# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 14:30:57 2020

@author: Firo Obeid
"""
from Obeid_Sentiment_Analysis import last 
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators, IntegerField
from time import sleep
import sqlite3
import os
import numpy as np


app = Flask(__name__)

class ReviewForm(Form):
    keyword = TextAreaField('Please Enter Tweet Keyword(ie: Weather, Bitcoin, EUR...):',[validators.DataRequired(),validators.length(min=1)])
    integer = IntegerField('Please Enter the number of latest tweet to run analysis on(ie:1,1000...):',[validators.DataRequired()])
    
@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)
@app.route('/results', methods=['POST', 'GET'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        tweet = form.keyword.data
        number = form.integer.data
        tweets, ptweets, ntweets, plist, nlist = last(tweet, number)
        positive = round(100*len(ptweets)/len(tweets), 4)
        negative = round(100*len(ntweets)/len(tweets), 4)
        neutral = round(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets),4)
    return render_template('results.html', tweet=tweet, lenp = len(plist), lenn = len(nlist), positive = positive, negative = negative, neutral = neutral, plist = plist, nlist = nlist)
    return render_template('reviewform.html', form=form)
    sleep(0.5)

if __name__ == '__main__':
    app.run(debug=True)