from application import app
from flask import Flask, render_template, request, flash, redirect, url_for,session
import sqlite3
ratings_ = [{'Rating': 1.0,'Name': "test1"},
            {'Rating': 2.0,'Name': "test2"},
            {'Rating': 3.0,'Name': "test3"}]

preds_ = [{'Predicted_Rating': 3.0,'Name': "test1"},
            {'Predicted_Rating': 3.0,'Name': "test2"},
            {'Predicted_Rating': 3.0,'Name': "test3"}]

app.secret_key='eezahahabuak'

con=sqlite3.connect('database.db')
con.execute("create table if not exists customer(pid integer primary key,name text,email text)")
con.close()

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

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect('database.db')
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute('select * from customer where name=? and email=?',(name,password))
        data=cur.fetchone()

        if data:
            session['name']=data['name']
            session['email']=data['email']
            return redirect('welcome')
        else:
            flash('Username and Password Mismatch','danger')
    
    return render_template("login.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            email=request.form['email']
            con=sqlite3.connect('database.db')
            cur=con.cursor()
            cur.execute('insert into customer(name,email)values(?,?)',(name,email))
            con.commit()
            flash("Record Added Successfully","success")
        except:
            flash('Error in insert operation','danger')
        finally:
            con.close()
    return render_template("register.html")