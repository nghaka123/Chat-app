from flask import Flask, render_template, request, redirect, session
import pyrebase
import os

app = Flask(__name__)
app.secret_key = "secret123"

config = {
  "apiKey": os.getenv("API_KEY"),
  "authDomain": os.getenv("AUTH_DOMAIN"),
  "projectId": os.getenv("PROJECT_ID"),
  "storageBucket": os.getenv("STORAGE_BUCKET"),
  "messagingSenderId": os.getenv("SENDER_ID"),
  "appId": os.getenv("APP_ID"),
  "databaseURL": os.getenv("DATABASE_URL")
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
