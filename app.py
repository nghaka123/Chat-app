from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import eventlet
import os

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

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
button:hover{background:#0056b3}
p{margin:5px 0}
</style>
</head>
<body>
<h2>Ka Chat App - Live Chat</h2>
<div id="chat"></div>
<div id="input-box">
<input id="msg" placeholder="Thu ziak rawh..." autocomplete="off">
<button onclick="send()">Thawn</button>
</div>

<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<script>
var socket = io();

function send(){
  let m = document.getElementById("msg").value;
  if(m){
    socket.emit('message', m);
    document.getElementById("msg").value = "";
  }
}

socket.on('message', function(msg){
  document.getElementById("chat").innerHTML += "<p><b>Mi dang:</b> "+msg+"</p>";
  document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight;
});

document.getElementById("msg").addEventListener("keypress", function(e){
  if(e.key === "Enter") send();
});
</script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@socketio.on('message')
def handle_message(msg):
    emit('message', msg, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
