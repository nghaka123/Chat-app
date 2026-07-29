import os
import pyrebase
from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY","secret123")

config = {
  "apiKey": os.environ.get("API_KEY"),
  "authDomain": os.environ.get("AUTH_DOMAIN"),
  "databaseURL": os.environ.get("DATABASE_URL"),
  "projectId": os.environ.get("PROJECT_ID"),
  "storageBucket": os.environ.get("STORAGE_BUCKET"),
  "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
  "appId": os.environ.get("APP_ID")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

storage = firebase.storage() # <- HEI HI BELH
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            auth.sign_in_with_email_and_password(email, password)
            session["user"] = email
            return redirect("/chat")
        except:
            return render_template("login.html", error="Email or Password dik lo")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect("/")
        except:
            return render_template("signup.html", error="Email a awm tawh a niang")
    return render_template("signup.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        try:
            auth.send_password_reset_email(email)
            return render_template("forgot.html", msg="Email ah reset link kan thawn")
        except:
            return render_template("forgot.html", error="Email a awm lo")
    return render_template("forgot.html")

@app.route("/chat")
def chat_page():
    if "user" not in session:
        return redirect("/")
    return render_template("chat.html", user=session["user"], config=config)

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/logout')
def logout():
    session.clear()  # session delete vek
    return redirect(url_for('login')) # login page ah let

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/setting')
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect('/setting')
    
    if file:
        filename = secure_filename(file.filename)
        # Firebase storage ah upload
        storage.child("profile_pics/" + session.get('user_id', 'user') + ".jpg").put(file)
        url = storage.child("profile_pics/" + session.get('user_id', 'user') + ".jpg").get_url(None)
        session['profile_pic'] = url # URL kan save
        return redirect('/setting')
