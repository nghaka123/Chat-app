from flask import Flask, render_template, request, redirect, url_for, session, flash
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = "chatapp123"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    if 'user' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"]) # <-- hei hi awm ngei tur
def login():
    return "Login page - HTML file la siam lo" # Tuna tan chuan tiang hian dah la


@app.route("/signup", methods=["GET", "POST"]) # <-- hei pawh
def signup():
    return "Signup page - HTML file la siam lo"


@app.route("/chat") # <-- hei pawh
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"Welcome {session['user']} - Chat page"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))
