import os
from flask import Flask, render_template, request, redirect, session
import firebase_admin
from firebase_admin import credentials, auth, db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "secret123")

# Firebase Admin init
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": os.environ.get("PROJECT_ID"),
  "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
  "private_key": os.environ.get("PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": os.environ.get("CLIENT_EMAIL"),
  "client_id": os.environ.get("CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
})
firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ.get("DATABASE_URL")
})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    try:
        user = auth.create_user(email=email, password=password)
        session["user"] = email
        return redirect("/chat")
    except:
        return "Signup a hlawhtling lo"

@app.route("/login", methods=["POST"])
def login():
    # firebase-admin hian login direct a nei lo. Kan awlsam nan session chiah kan dah
    session["user"] = request.form["email"]
    return redirect("/chat")

@app.route("/chat")
def chat_page():
    if "user" in session:
        return render_template("chat.html", user=session["user"], config={
            "apiKey": os.environ.get("API_KEY"),
            "authDomain": os.environ.get("AUTH_DOMAIN"),
            "databaseURL": os.environ.get("DATABASE_URL"),
            "projectId": os.environ.get("PROJECT_ID")
        })
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
