import os
import pyrebase
from flask import Flask, render_template, request, redirect, session, flash, url_for

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
db = firebase.database() # <-- HEI HI BELH

storage = firebase.storage()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if "user" in session:
        return redirect('/users')
    else:
        return redirect('/login')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            auth.sign_in_with_email_and_password(email, password)
            session["user"] = email
            return redirect("/users") # <-- HEI HI THLAK /chat ai ah
        except:
            return render_template("login.html", error="Email or Password dik lo")
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = None
    msg_type = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user_with_email_and_password(email, password)
            # User list ah save bawk
            db.child("users").child(email.replace(".", ",")).set({"email": email})
            message = "Signup Successful! Please Login"
            msg_type = "success"
        except:
            message = "Email hi a lo awm tawh"
            msg_type = "error"
    return render_template('signup.html', message=message, msg_type=msg_type)

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

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/users')
def users():
    if "user" not in session:
        return redirect('/login')

    # Firebase atangin user zawng zawng la
    all_users = db.child("users").get().val()
    
    # User an la awm loh chuan dict ruak ah chantir
    if all_users is None:
        all_users = {}
        
    return render_template('users.html', users=all_users, me=session['user'])

@app.route('/chat/<room_id>', methods=['GET', 'POST'])
def private_chat(room_id):
    if "user" not in session:
        return redirect('/login')

    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            db.child("private_chats").child(room_id).push({
                "user": session['user'],
                "text": message
            })
        return redirect(f'/chat/{room_id}')

    messages = db.child("private_chats").child(room_id).get().val()
    msg_list = []
    if messages:
        for key, val in messages.items():
            msg_list.append(val)

    # config pass a ngai bawk
    return render_template('chat.html',
                           messages=msg_list,
                           user=session['user'],
                           room_id=room_id,
                           config=config)
