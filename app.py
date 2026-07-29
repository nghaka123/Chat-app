from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = "chatapp123"

# Supabase connect
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


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
    
    # Message zawng zawng lak chhuah
    try:
        messages = supabase.table("messages").select("*").order("created_at").execute()
        messages_data = messages.data
    except:
        messages_data = []
    
    return render_template("chat.html", user=session['user'], messages=messages_data)


@app.route("/send", methods=["POST"])
def send():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    message = request.form["message"]
    user = session['user']
    
    # Supabase ah save
    supabase.table("messages").insert({
        "user": user,
        "message": message
    }).execute()
    
    return redirect(url_for("chat"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
