from application import app
from flask import Flask, render_template, request, flash, redirect, url_for,session

ratings_ = [{'Rating': 1.0,'Name': "test1"},
            {'Rating': 2.0,'Name': "test2"},
            {'Rating': 3.0,'Name': "test3"}]

preds_ = [{'Predicted_Rating': 3.0,'Name': "test1"},
            {'Predicted_Rating': 3.0,'Name': "test2"},
            {'Predicted_Rating': 3.0,'Name': "test3"}]

@app.route("/")
def index():
    return render_template("index.html", navindex=True)

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", navcatalog=True)

@app.route("/recommend")
def recommend():
    return render_template("recommend.html", navrecommend=True, predictions=preds_)

@app.route("/reviews")
def reviews():
    return render_template("reviews.html", navreviews=True, ratings=ratings_)

@app.route("/about")
def about():
    return render_template("about.html", navabout=True)

@app.route("/login")
def login():
    return render_template("login.html", navlogin=True)

@app.route("/register",methods=['GET','POST'])
def register():
    return render_template("register.html")
