import os
import pyrebase
from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "secret123") # Render ah kan set ang

# Render Environment Variable atanga la vek tur
firebaseConfig = {
  "apiKey": os.environ.get("API_KEY"),
  "authDomain": os.environ.get("AUTH_DOMAIN"),
  "databaseURL": os.environ.get("DATABASE_URL"),
  "projectId": os.environ.get("PROJECT_ID"),
  "storageBucket": os.environ.get("STORAGE_BUCKET"),
  "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
  "appId": os.environ.get("APP_ID")
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        auth.create_user_with_email_and_password(email, password) # Error a awm chuan a tlu nghal ang
        return redirect("/")
    return render_template("signup.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    auth.sign_in_with_email_and_password(email, password) # Error a awm chuan a tlu nghal ang
    session["user"] = email
    return redirect("/chat")

@app.route("/chat")
def chat_page():
    if "user" in session:
        # config zawng zawng html ah thawn chhuk
        config = {
            "apiKey": os.environ.get("API_KEY"),
            "authDomain": os.environ.get("AUTH_DOMAIN"),
            "databaseURL": os.environ.get("DATABASE_URL"),
            "projectId": os.environ.get("PROJECT_ID")
        }
        return render_template("chat.html", user=session["user"], config=config)
    return redirect("/")

@app.route("/send", methods=["POST"])
def send_message():
    if "user" in session:
        message = request.form["message"]
        db = firebase.database()
        db.child("messages").push({"user": session["user"], "text": message})
    return redirect("/chat")

from datetime import datetime

@app.route("/chat/<room>")
def chat_room(room):
    if "user" in session:
        config = {
            "apiKey": os.environ.get("API_KEY"),
            "authDomain": os.environ.get("AUTH_DOMAIN"),
            "databaseURL": os.environ.get("DATABASE_URL"),
            "projectId": os.environ.get("PROJECT_ID")
        }
        return render_template("chat.html", user=session["user"], room=room, config=config)
    return redirect("/")

@app.route("/send/<room>", methods=["POST"])
def send_message_room(room):  # <-- Hming hi thlak
    if "user" in session:
        message = request.form["message"]
        db = firebase.database()
        db.child("rooms").child(room).child("messages").push({
            "user": session["user"], 
            "text": message,
            "time": datetime.now().strftime("%H:%M")
        })
    return redirect(f"/chat/{room}")
