from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

HTML = '''
<!doctype html>
<html>
<head><title>Ka Chat App</title>
<style>
body{font-family:Arial; padding:20px; background:#f0f0f0}
#chat{border:1px solid #ccc; height:400px; overflow-y:scroll; padding:10px; background:white; margin-bottom:10px}
input{width:80%; padding:10px}
button{padding:10px 20px; background:#007bff; color:white; border:none}
</style>
</head>
<body>
<h2>Ka Chat App - Live Chat</h2>
<div id="chat"></div>
<input id="msg" placeholder="Thu ziak rawh...">
<button onclick="send()">Thawn</button>

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
    socketio.run(app, host="0.0.0.0", port=10000)    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
