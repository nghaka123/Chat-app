from flask import Flask, render_template_string, request, jsonify
import os
app = Flask(__name__)
messages = []

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
.box{background:white; padding:20px; border-radius:8px; text-align:center}
button{padding:12px 20px; background:#007bff; color:white; border:none; border-radius:5px; cursor:pointer}
#chat{border:1px solid #ccc; height:350px; overflow-y:scroll; padding:10px; background:white; margin-bottom:10px; border-radius:8px}
p{margin:5px 0; padding:10px; border-radius:10px; max-width:70%}
.me{background:#d1e7ff; margin-left:auto; text-align:right}
.other{background:#e9ecef; margin-right:auto; text-align:left}
</style>
</head>
<body>
<div class="nav">
<a href="/">Home</a> | 
<a href="/chat">Chat</a> | 
<a href="/settings">Settings</a> | 
<a href="/about">About</a>
</div>
{{ content|safe }}
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

# I CHAT leh SETTINGS code hlui kha hetah dah rawh
CHAT_HTML = '''...i chat code v8.0 kha...'''
SETTING_HTML = '''...i settings code v9.0 kha...'''

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

@app.route("/messages")
def get_messages():
    return jsonify(messages)

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()
    messages.append((data['name'], data['msg']))
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
