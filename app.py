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
db = firebase.database()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat")
def chat_page():
    if "user" in session:
        return render_template("chat.html", user=session["user"])
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
