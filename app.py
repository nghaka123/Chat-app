from flask import Flask, render_template_string
import os
app = Flask(__name__)

BASE_HTML = '''
<!doctype html>
<html>
<head>
<title>Ka Chat App</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{font-family:Arial; padding:20px; background:#f0f0f0; margin:0}
.nav{text-align:center; margin-bottom:15px; background:white; padding:10px; border-radius:8px}
.nav a{margin:0 10px; text-decoration:none; color:#007bff; font-weight:bold}
.nav a:hover{text-decoration:underline}
.box{background:white; padding:20px; border-radius:8px}
</style>
</head>
<body>
<div class="nav">
<a href="/">Home</a> | 
<a href="/chat">Chat</a> | 
<a href="/settings">Settings</a> | 
<a href="/about">About</a>
</div>
{{content}}
</body>
</html>
'''

HOME_HTML = '''
<div class="box">
<h2>Welcome to Ka Chat App</h2>
<p>He mi app hi kan siam chhin na a ni. Message in thawn thei.</p>
<a href="/chat"><button>Chat na ah lut rawh</button></a>
</div>
'''

ABOUT_HTML = '''
<div class="box">
<h2>About</h2>
<p>He app hi Flask + Render hmang a siam a ni.</p>
<p>Siama tu: Nangmah 😎</p>
</div>
'''

# I chat leh settings code hlui kha hetah dah zel
CHAT_HTML = ''' ... i chat code hlui ... '''
SETTING_HTML = ''' ... i settings code hlui ... '''

@app.route("/")
def home():
    return render_template_string(BASE_HTML, content=HOME_HTML)

@app.route("/chat")
def chat():
    return render_template_string(BASE_HTML, content=CHAT_HTML)

@app.route("/settings")
def settings():
    return render_template_string(BASE_HTML, content=SETTING_HTML)

@app.route("/about")
def about():
    return render_template_string(BASE_HTML, content=ABOUT_HTML)

# /messages, /send, /clear api te pawh a ngai tho
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
