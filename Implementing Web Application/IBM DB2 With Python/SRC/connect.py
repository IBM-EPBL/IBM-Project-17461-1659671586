# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 20:47:19 2022

@author: SRI GAYATHIRI
"""
from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re

app=Flask(__name__)
app.secret_key='a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zvl42723;PWD=hXf4RGalRBp2sQU6",'','')

@app.route('/')
def home():
    return render_template('index.html')

if __name__=='__main__':
    app.run(host='0.0.0.0')