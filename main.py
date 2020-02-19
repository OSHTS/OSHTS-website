from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "nothing"
db = SQLAlchemy(app)

def hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), unique=False, nullable=False, default="Anonymous")
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default="default.jpg" )


    def __repr__(self):
        f"fullname:{slef.fullname}, username:{self.username}, id:{self.id}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/forume")
def courses():
    return render_template("forume.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = hash(request.form['password'])

        user = User.query.filter_by(username=username)
        if user is not None:
            user = user[0]
            if password == user.password:
                return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        fullname = request.form['fullname']
        username = request.form['username']
        password = hash(request.form['password'])

        user = User(fullname=fullname, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))


    return render_template("signup.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
