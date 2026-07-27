from flask import Flask, render_template_string, request, redirect
import os

app = Flask(__name__)
messages = []

HTML = '''
<!doctype html>
<html>
<head>
<title>Ka Chat App</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="3">
<style>
body{font-family:Arial; padding:20px; background:#f0f0f0; margin:0}
h2{text-align:center; color:#333}
#chat{border:1px solid #ccc; height:350px; overflow-y:scroll; padding:10px; background:white; margin-bottom:10px; border-radius:8px}
#input-box{display:flex; flex-direction:column; gap:10px}
.input-row{display:flex; gap:10px}
input{flex:1; padding:12px; border:1px solid #ccc; border-radius:5px}
button{padding:12px 20px; background:#007bff; color:white; border:none; border-radius:5px; cursor:pointer}
button:hover{background:#0056b3}
p{margin:5px 0; padding:8px; background:#d1e7ff; border-radius:5px}
b{color:#004085}
</style>
</head>
<body>
<h2>Ka Chat App - Live Chat</h2>
<div id="chat">
{% for name, msg in messages %}
<p><b>{{ name }}:</b> {{ msg }}</p>
{% endfor %}
</div>
<form method="POST" id="input-box">
<div class="input-row">
<input name="name" placeholder="I hming ziak rawh" required style="width:120px; flex:0.3">
<input name="msg" placeholder="Thu ziak rawh..." autocomplete="off" required>
</div>
<button type="submit">Thawn</button>
</form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        msg = request.form.get("msg")
        if name and msg:
            messages.append((name, msg))
        return redirect("/")
    return render_template_string(HTML, messages=messages)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
