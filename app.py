from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Chat App is Running on Render!" 

@app.route("/chat")
def chat():
    return render_template("index.html") # I HTML file awm chuan

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)