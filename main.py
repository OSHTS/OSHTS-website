from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import login_required, logout_user, current_user, login_user, UserMixin
import hashlib
import json

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

Fetched = db.Table("Fetched",
    db.Column("user_id",db.Integer, db.ForeignKey("user.id")),
    db.Column("message_id",db.Integer, db.ForeignKey("message.id"))
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), unique=False, nullable=False, default="Anonymous")
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default="default.jpg" )
    seen = db.relationship("Message", secondary=Fetched, backref=db.backref("Chatters",lazy="dynamic") )

    def __repr__(self):
        return f"User('{self.id}', '{self.fullname}', '{self.username}')"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300))


    def __repr__(self):
        return f"User('{self.id}')"

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
            else:
                flash("You entered the wrong password", "error")
                return render_template("login.html")
        flash("Account does not exit", "error")
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        fullname = request.form['fullname']
        username = request.form['username']
        password = hash(request.form['password'])
        c_password = hash(request.form['c_password'])

        user = User.query.filter_by(username=username).first()

        if user is None:
            if password == c_password:
                user = User(fullname=fullname, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                new_user = User.query.filter_by(username=username).first()
                login_user(new_user)
                return redirect(url_for('index'))
            else:
                flash("Password does not match your confirmed password", "error")
                return render_template("signup.html")
        else:
            flash("Username has been taken already")
            return render_template("signup.html")
    return render_template('signup.html')


@app.route("/chatroom")
def chatroom():
    return render_template('chatroom.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/messages")
def messages():
    #if user has logged in, then it retrives new messages unread by user
    if current_user.is_authenticated:
        c_user = current_user
        #Queryinh all datanbase messages
        messages = Message.query.all()
        #variables to hold te messages for iteration
        db_messages = []
        n_messages = []
        #Variable to hold filtered messages
        api_messages = []
        for message in messages:
            db_messages.append(message)
        if(db_messages != []):
            #if messages in the database is nt empty, then
            for x in db_messages:
                if(c_user in x.Chatters):
                    #Checking if user has seen the message then skip
                    pass
                else:
                    #else append the message as unread
                    n_messages.append(x)
        #Converting messages from Type Object to Type Dictionary
        for message in n_messages:
            new_messages = {}
            new_messages['message'] = message.message
            new_messages['id'] = message.id
            api_messages.append(new_messages)
        #return json.dumps(api_messages)
        return jsonify(api_messages)
    return redirect(url_for('index'))

@app.route("/send_msg/<int:id>")
def send_msg(id):
    if current_user.is_authenticated:
        user = current_user
        message = Message.query.get(id)
        message.Chatters.append(user)
        db.session.commit()
        return jsonify({'success':True})
    return redirect(url_for('login'))

@app.route("/post_msg/<message>")
def post_msg(message):
    if current_user.is_authenticated:
        user = current_user
        msg = Message(message=message)
        db.session.add(msg)
        msg.Chatters.append(user)
        db.session.commit()
        return jsonify({'success': True})
    return redirect(url_for('login'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
