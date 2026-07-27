from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import eventlet
import os

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', transports=['polling'])

HTML = '''
<!doctype html>
<html>
<head>
<title>Ka Chat App</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{font-family:Arial; padding:20px; background<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
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
