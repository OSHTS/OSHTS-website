from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import login_required, logout_user, current_user, login_user, UserMixin
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}'.format(
#       username="OSHTS",
#       password="TECHnical2233",
#       hostname="OSHTS.mysql.pythonanywhere-services.com,
#       databasename="oshts_db"

#)
app.config['SECRET_KEY'] = "nothing"
db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


class User(db.Model, UserMixin):
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        username = request.form['username']
        password = hash(request.form['password'])

        user = User.query.filter_by(username=username).first()
        if user is not None:
            if password == user.password:
                login_user(user)
                return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        fullname = request.form['fullname']
        username = request.form['username']
        password = hash(request.form['password'])

        user = User(fullname=fullname, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template("signup.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
