import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client

app = Flask(__name__)

# Hei hi i URL leh KEY tak tak dah rawh
SUPABASE_URL = "https://dytydxoihelpgtsavsb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5dHl0ZHhvaWhlbHBndGF2c3ZiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUxNTQwNjksImV4cCI6MjEwMDczMDA2OX0.ShuZ_oFuZPDXhjzPMV4GDOYk1qarjOJUfXPxafVjdSA"  # i anon key sei deuh

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        action = request.form["action"]
        try:
            if action == "signup":
                res = supabase.auth.sign_up({"email": email, "password": password})
                flash("Signup tluang! Email ah confirm la")
            elif action == "login":
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                session["user"] = res.user.email
                return redirect(url_for("chat"))
        except Exception as e:
            flash(f"Error: {str(e)}")
    return render_template("index.html")

@app.route("/chat")
def chat():
    if "user" not in session: return redirect(url_for("home"))
    return render_template("chat.html", user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
