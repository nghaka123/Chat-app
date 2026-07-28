import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "test_secret_key_12345")

# STEP 1: Render Env atangin kan la - Direct dah suh
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Check na: Env a kosong chuan app a tlan dawn lo
if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL or SUPABASE_KEY is missing in Environment Variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        action = request.form["action"]

        try:
            if action == "signup":
                res = supabase.auth.sign_up({"email": email, "password": password})
                flash("Signup tluang! Email ah confirm link a kal ang")
            elif action == "login":
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                session["user"] = res.user.email
                return redirect(url_for("chat"))
        except Exception as e:
            flash(f"Error: {str(e)}")
    
    return render_template("index.html")


@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("chat.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logout i tluang")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
