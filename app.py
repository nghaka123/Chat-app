from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# ========== FIREBASE CONNECT ==========
try:
    firebase_key = os.environ.get('FIREBASE_KEY')
    if firebase_key:
        key_dict = json.loads(firebase_key)
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase Connected Successfully!")
    else:
        print("FIREBASE_KEY not found in Environment")
        db = None
except Exception as e:
    print("Firebase Error:", e)
    db = None
# =======================================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session["username"] = username
            return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "username" not in session:
        return redirect(url_for("login"))

    if db is None:
        return "Firebase not connected. Check FIRE
