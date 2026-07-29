from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore
import json, os
from datetime import datetime

app = Flask(__name__)  # <-- Hei hi a pawimawh ber
app.secret_key = "secret123"  # Password atan, engpawh i dah thei

# ========== FIREBASE CONNECT ==========
try:
    key_dict = json.loads(os.environ.get('FIREBASE_KEY'))
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase Connected Successfully!")
except Exception as e:
    print("Firebase Error:", e)
    db = None
# =======================================


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
