from application import app
from flask import render_template

ratings_ = [{'Rating': 1.0,'Name': "test1"},
            {'Rating': 2.0,'Name': "test2"},
            {'Rating': 3.0,'Name': "test3"}]

@app.route("/")
def index():
    return render_template("index.html", navindex=True)

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", navcatalog=True)

@app.route("/recommend")
def recommend():
    return render_template("recommend.html", navrecommend=True)

@app.route("/reviews")
def reviews():
    return render_template("reviews.html", navreviews=True, ratings=ratings_)

@app.route("/about")
def about():
    return render_template("about.html", navabout=True)

@app.route("/login")
def login():
    return render_template("login.html", navlogin=True)