from application import app

@app.route("/")
def index():
    return '<h1>Test !</h1>'