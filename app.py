from flask import Flask, render_template, request, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, firestore
import json, os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# ========== FIREBASE CONNECT ==========
db = None
try:
    firebase_key = os.environ.get('FIREBASE_KEY')
    if firebase_key:
        key_dict = json.loads(firebase_key)
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase Connected Successfully!")
except Exception as e:
    print("Firebase Error:", e)
# =======================================

@app.route("/", methods=["GET", "POST"])
def login():
    if db is None:
        return "ERROR: Firebase not connected. Check FIREBASE_KEY in Render Environment"

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # User zawng
        user_ref = db.collection("users").document(username).get()
        if user_ref.exists:
            user_data = user_ref.to_dict()
            if check_password_hash(user_data["password"], password):
                session["username"] = username
                return redirect(url_for("chat"))

        flash("Username or Password a dik lo")
        return redirect(url_for("login")) # <-- heihi kan belh

    return render_template("login.html") # <-- heihi a tawp ber ah a awm ngei tur
