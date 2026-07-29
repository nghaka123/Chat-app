from flask import Flask, render_template, request, redirect, session, flash
import pyrebase
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# Render Environment Variable atangin a la dawn
config = {
  "apiKey": os.getenv("API_KEY"),
  "authDomain": os.getenv("AUTH_DOMAIN"),
  "projectId": os.getenv("PROJECT_ID"),
  "storageBucket": os.getenv("STORAGE_BUCKET"),
  "messagingSenderId": os.getenv("SENDER_ID"),
  "appId": os.getenv("APP_ID"),
  "databaseURL": os.getenv("DATABASE_URL")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            auth.create_user_with_email_and_password(email, password)
            flash("Account siam a tling e! Tun ah login rawh", "success")
            return redirect("/")
        except:
            flash("Email hi a lo awm sa tawh", "danger")
            return redirect("/signup")
    return render_template("signup.html")

@app.route("/", methods=["GET"])  # GET chiah phal
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"]) # POST chiah phal
def login():
    email = request.form["email"]
    password = request.form["password"]
    try:
        auth.sign_in_with_email_and_password(email, password)
        session["user"] = email
        return redirect("/chat")
    except:
        flash("Email emaw Password emaw a dik lo", "danger")
        return redirect("/")

@app.route("/chat")
def chat():
    if "user" in session:
        return render_template("chat.html", user=session["user"])
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
