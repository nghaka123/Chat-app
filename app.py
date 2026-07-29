import os
import pyrebase
from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = "secret123"

# I Firebase Project Settings atanga copy rawh
firebaseConfig =  {
  apiKey: "AIzaSyBqnSp9piRhHBTyBUwIFOs2_U08LpWOj8g",
  authDomain: "chat-app-1dc73.firebaseapp.com",
  databaseURL: "https://chat-app-1dc73-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "chat-app-1dc73",
  storageBucket: "chat-app-1dc73.firebasestorage.app",
  messagingSenderId: "777889797353",
  appId: "1:777889797353:web:724827b1d1cd7ab3144c78",
  measurementId: "G-ZRK14W39BV"
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
        return render_template("chat.html", user=session["user"])
    return redirect("/")
