from application import app
from flask import render_template, url_for

@app.route("/")
def index():
    return render_template("index.html", navindex=True)

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", navcatalog=True)

@app.route("/recommend")
def recommend():
    return render_template("recommend.html", navrecommend=True)