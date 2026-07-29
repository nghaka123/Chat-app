from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, session
import pyrebase

app = Flask(__name__)
app.secret_key = "secret123"

config = {
    "apiKey": os.environ.get("API_KEY"),
    "authDomain": os.environ.get("AUTH_DOMAIN"),
    "databaseURL": os.environ.get("DATABASE_URL"),
    "projectId": os.environ.get("PROJECT_ID"),
    "storageBucket": os.environ.get("STORAGE_BUCKET"),
    "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
    "appId": os.environ.get("APP_ID")
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat")
def chat_page():
    if "user" in session:
        config = {
            "apiKey": os.environ.get("API_KEY"),
            "authDomain": os.environ.get("AUTH_DOMAIN"),
            "databaseURL": os.environ.get("DATABASE_URL"),
            "projectId": os.environ.get("PROJECT_ID")
        }
        return render_template("chat.html", user=session["user"], config=config)
    return redirect("/")

@app.route("/send", methods=["POST"])  # room bo tawh
def send_message():
    if "user" in session:
        message = request.form["message"]
        db.child("messages").push({
            "user": session["user"], 
            "text": message,
            "time": datetime.now().strftime("%H:%M")
        })
    return redirect("/chat")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    try:
        auth.sign_in_with_email_and_password(email, password)
        session["user"] = email
        return redirect("/chat")
    except:
        return "Login a hlawhtling lo. Email/password check leh rawh"

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    try:
        auth.create_user_with_email_and_password(email, password)
        session["user"] = email
        return redirect("/chat")
    except:
        return "Signup a hlawhtling lo. Email a awm tawh ani thei"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/")
def home():
    return "<h1 style='text-align:center; margin-top:100px;'>App a thawk</h1><br><a href='/chat'>Chat ah kal</a>"
