import os
import pyrebase
from flask import Flask, render_template, request, redirect, session, flash, url_for

def safe_key(email):
    return email.replace('.', ',') #. chu, ah kan thlak

def get_room_id(user1, user2):
    # Tu hmasa pawh ni se room name a inang vek tur - A pawimawh ber
    users = sorted([safe_key(user1), safe_key(user2)])
    return f"{users[0]}_{users[1]}"

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
db = firebase.database()
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
            return redirect("/users")
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
            db.child("users").child(safe_key(email)).set({"email": email})
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

    all_users = db.child("users").get().val()
    if all_users is None:
        all_users = {}

    return render_template('users.html', users=all_users, me=session['user'])

@app.route('/chat/<other_user>', methods=['GET', 'POST']) # room_id → other_user
def chat(other_user):
    if "user" not in session:
        return redirect('/login')

    me = session['user']
    me_safe = safe_key(me)
    room = get_room_id(me, other_user) # HEI HI NGAI PAWIMAWH

    if request.method == 'POST':
        msg = request.form['message']
        db.child("private_chats").child(room).push({
            "sender": me_safe,
            "message": msg,
            "time": {".sv": "timestamp"}
        })
        return redirect(f'/chat/{other_user}')

    messages_data = db.child("private_chats").child(room).get().val()
    messages = []
    if messages_data:
        for key, val in messages_data.items():
            val['id'] = key
            messages.append(val)

    return render_template('chat.html', messages=messages, me=me_safe, room=other_user)
