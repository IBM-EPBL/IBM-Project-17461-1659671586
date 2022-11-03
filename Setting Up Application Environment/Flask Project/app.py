# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 18:26:55 2022

@author: SRI GAYATHIRI
"""

from flask import Flask,render_template,request
app=Flask(__name__)
@app.route('/')
def display():
    return render_template("display.html")
if __name__==('__main__'):
    app.run(debug=True)