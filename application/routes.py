from application import app
from flask import Flask, render_template, request, flash, redirect, url_for,session
import sqlite3
from functools import wraps
from math import ceil

app.secret_key='eezahahabuak'

con=sqlite3.connect('database.db')
con.execute("create table if not exists customer(pid integer primary key,name text,password integer)")
con.close()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

@app.route("/")
def index():
    return render_template("index.html", navindex=True)

@app.route("/recommend")
@login_required
def recommend():
    # Connect to the movie database
    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Retrieve movie data from the database
    cur.execute('SELECT title, overview, vote_average FROM movie')
    movies = cur.fetchall()
    con.close()

    # Pass the movie data to the recommend.html template
    return render_template("recommend.html", navrecommend=True, movies=movies)

@app.route("/toprated")
@login_required
def toprated():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Count total number of movies
    cur.execute('SELECT COUNT(*) FROM movie')
    total_count = cur.fetchone()[0]

    # Calculate total pages
    total_pages = ceil(total_count / per_page)

    # Retrieve movies for the current page
    cur.execute('SELECT title, release_date, vote_average FROM movie ORDER BY vote_average DESC LIMIT ? OFFSET ?', (per_page, (page - 1) * per_page))
    movies = cur.fetchall()
    con.close()

    return render_template("toprated.html", movies=movies, navtoprated=True, total_pages=total_pages, current_page=page)

@app.route("/newrelease")
@login_required
def newrelease():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Count total number of movies
    cur.execute('SELECT COUNT(*) FROM movie')
    total_count = cur.fetchone()[0]

    # Calculate total pages
    total_pages = ceil(total_count / per_page)

    # Retrieve movies for the current page
    cur.execute('SELECT title, release_date, vote_average FROM movie ORDER BY release_date DESC LIMIT ? OFFSET ?', (per_page, (page - 1) * per_page))
    movies = cur.fetchall()
    con.close()

    return render_template("newrelease.html", movies=movies, navnewrelease=True, total_pages=total_pages, current_page=page)

@app.route("/popularity")
@login_required
def popularity():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Count total number of movies
    cur.execute('SELECT COUNT(*) FROM movie')
    total_count = cur.fetchone()[0]

    # Calculate total pages
    total_pages = ceil(total_count / per_page)

    # Retrieve movies for the current page
    cur.execute('SELECT title, vote_average, popularity, overview FROM movie ORDER BY popularity DESC LIMIT ? OFFSET ?', (per_page, (page - 1) * per_page))
    movies = cur.fetchall()
    con.close()

    return render_template("popularity.html", movies=movies, navpopularity=True, total_pages=total_pages, current_page=page)

@app.route("/about")
@login_required
def about():
    return render_template("about.html", navabout=True)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        con = sqlite3.connect('movies.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        # Perform search query against the database
        cur.execute("""
            SELECT movie.title, movie.overview, person.person_name
            FROM movie 
            JOIN movie_cast ON movie.movie_id = movie_cast.movie_id 
            JOIN person ON movie_cast.person_id = person.person_id 
            WHERE movie.title LIKE ? OR movie.overview LIKE ? OR person.person_name LIKE ?
        """, ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
        
        movies = cur.fetchall()
        con.close()
        return render_template("search.html", navsearch=True, search_page=True, movies=movies, query=query)
    else:
        return render_template("search.html", navsearch=True, search_page=True)

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect('database.db')
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute('select * from customer where name=? and password=?',(name,password))
        data=cur.fetchone()

        if data:
            session['name']=data['name']
            session['password']=data['password']
            return redirect('/')
        else:
            flash('Username and Password Mismatch','danger')
    
    return render_template("login.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            password=request.form['password']
            con=sqlite3.connect('database.db')
            cur=con.cursor()
            cur.execute('insert into customer(name,password)values(?,?)',(name,password))
            con.commit()
            flash("Record Added Successfully","success")
            return redirect(url_for('login'))
        except:
            flash('Error in insert operation','danger')
        finally:
            con.close()
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/welcome',methods=["GET","POST"])
@login_required
def welcome():
    return render_template('welcome.html')