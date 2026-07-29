from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore
import json, os
from datetime import datetime

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
    else:
        print("FIREBASE_KEY not found in Environment")
except Exception as e:
    print("Firebase Error:", e)
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
        return "ERROR: Firebase not connected. Check FIREBASE_KEY in Render Environment tab" # <-- return kan dah

    # Message thawn
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            db.collection("messages").add({
                "user": session["username"],
                "text": message,
                "time": datetime.now()
            })
        return redirect(url_for("chat"))

    # Message lak chhuah
    messages = []
    try:
        messages_ref = db.collection("messages").order_by("time").limit(50).stream()
        for msg in messages_ref:
            msg_data = msg.to_dict()
            messages.append(msg_data)
    except Exception as e:
        print("Error fetching messages:", e)
        return f"Error loading messages: {e}" # <-- return kan dah

    return render_template("chat.html", username=session["username"], messages=messages) # <-- return kan dah


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
