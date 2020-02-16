from flask import Flask, render_template, url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:////database.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/forume")
def courses():
    return render_template("forume.html")

if __name__ == "__main__":
    app.run(debug=True)
