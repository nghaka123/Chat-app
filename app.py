from flask import Flask, render_template, request, redirect, url_for, flash, session
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = "ka_secret_key_thlak_la" # he mi hi thlak la

# STEP 1: I Supabase URL leh ANON KEY dah
SUPABASE_URL = "https://qytqsxawhq1ptqsviab.supabase.co"
SUPABASE_KEY = "b_a-pu4llshl_1n7DAMsU_sG61qSx7A_8HBF-1V" # I anon key full dah

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        action = request.form["action"]

        try:
            if action == "signup":
                # SIGNUP
                res = supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                if res.user:
                    flash("Signup a hlawhtling! Tun ah Login rawh", "success")
                else:
                    flash("Signup a hlawhtling lo: " + res.error.message, "error")

            elif action == "login":
                # LOGIN
                res = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                if res.user:
                    session["user"] = res.user.email
                    return redirect(url_for("chat"))
                else:
                    flash("Login a hlawhtling lo: " + res.error.message, "error")

        except Exception as e:
            flash("Error: " + str(e), "error")

    return render_template("index.html")


@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("chat.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    supabase.auth.sign_out()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
