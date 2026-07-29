from flask import Flask, render_template, request, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, firestore
import json, os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123_chat_app_key" # heihi thlak danglam thei

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
    else:
        print("FIREBASE_KEY not found in Environment Variables")
except Exception as e:
    print("Firebase Error:", e)
# =======================================
