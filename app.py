from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = '''
<!doctype html>
<html>
<head>
<title>Ka Chat App</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{font-family:Arial; padding:20px; background:#f0f0f0; margin:0}
h2{text-align:center; color:#333}
#chat{border:1px solid #ccc; height:400px; overflow-y:scroll; padding:10px; background:white; margin-bottom:10px; border-radius:8px}
#input-box{display:flex; gap:10px}
input{flex:1; padding:12px; border:1px solid #ccc; border-radius:5px}
button{padding:12px 20px; background:#007bff; color:white; border:none; border-radius:5px; cursor:pointer}
</style>
</head>
<body>
<h2>Ka Chat App - A Tluang Ta!</h2>
<div id="chat">
<p>Welcome! He mi hi a lang thei tawh tih na</p>
</div>
<div id="input-box">
<input id="msg" placeholder="Thu ziak rawh...">
<button>Thawn</button>
</div>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
