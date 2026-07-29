from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = "chatapp123"

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session['user'] = request.form["email"]
        return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

@app.route("/chat")
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("chat.html", user=session['user'], messages=[])

@app.route("/send", methods=["POST"])
def send():
    return redirect(url_for("chat"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
