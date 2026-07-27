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
.box{background:white; padding:20px; border-radius:8px; text-align:center}
button{padding:12px 20px; background:#007bff; color:white; border:none; border-radius:5px; cursor:pointer}
#chat{border:1px solid #ccc; height:350px; overflow-y:scroll; padding:10px; background:white; margin-bottom:10px; border-radius:8px; text-align:left}
.input-row{display:flex; gap:10px; margin-bottom:10px}
input{flex:1; padding:12px; border:1px solid #ccc; border-radius:5px}
p{margin:5px 0; padding:10px; border-radius:10px; max-width:70%; word-wrap:break-word}
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

CHAT_HTML = '''
<h2 style="text-align:center">Live Chat</h2>
<div id="chat"></div>
<div id="input-box">
<div class="input-row">
<input id="name" placeholder="I hming ziak rawh" required>
<input id="msg" placeholder="Thu ziak rawh..." autocomplete="off" required>
</div>
<button onclick="send()" style="width:100%">Thawn</button>
</div>

<script>
let myName = localStorage.getItem("myName") || "";
let myColor = localStorage.getItem("myColor") || "#d1e7ff";

function loadMessages(){
  fetch('/messages').then(r=>r.json()).then(data=>{
    let chat = document.getElementById("chat");
    chat.innerHTML = "";
    data.forEach(m=>{
      let className = (m[0] === myName)? "me" : "other";
      let style = (m[0] === myName)? `background:${myColor}` : "";
      chat.innerHTML += `<p class="${className}" style="${style}"><b>${m[0]}:</b> ${m[1]}</p>`;
    });
    chat.scrollTop = chat.scrollHeight;
  });
}

function send(){
  let name = document.getElementById("name").value;
  let msg = document.getElementById("msg").value;
  if(name && msg){
    localStorage.setItem("myName", name);
    myName = name;
    fetch('/send', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({name: name, msg: msg})
    }).then(()=> {
      document.getElementById("msg").value = "";
      loadMessages();
    });
  }
}

document.getElementById("msg").addEventListener("keypress", function(e){
  if(e.key === "Enter") send();
});

document.getElementById("name").value = myName;
loadMessages();
setInterval(loadMessages, 3000);
</script>
'''

SETTING_HTML = '''
<div class="box" style="text-align:left">
<h2>Settings</h2>
<h3>I hming thlak</h3>
<input id="setName" placeholder="Hming thar" style="width:100%; margin-bottom:10px">
<button onclick="saveName()">Save Hming</button>

<h3 style="margin-top:20px">I message color</h3>
<input type="color" id="setColor" value="#d1e7ff">
<button onclick="saveColor()">Save Color</button>

<h3 style="margin-top:20px">Chat Clear</h3>
<button onclick="clearChat()" style="background:red">Delete All Messages</button>
</div>

<script>
document.getElementById("setName").value = localStorage.getItem("myName") || "";
document.getElementById("setColor").value = localStorage.getItem("myColor") || "#d1e7ff";
function saveName(){
  let name = document.getElementById("setName").value;
  localStorage.setItem("myName", name);
  alert("Hming save tawh!");
}
function saveColor(){
  let color = document.getElementById("setColor").value;
  localStorage.setItem("myColor", color);
  alert("Color save tawh!");
}
function clearChat(){
  if(confirm("I delete duh takzet maw?")){
    fetch('/clear', {method:'POST'}).then(()=>alert("Delete zo"));
  }
}
</script>
'''

ABOUT_HTML = '''
<div class="box">
<h2>About</h2>
<p>He app hi Flask + Render hmang a siam a ni.</p>
<p>Siama tu: Nangmah 😎</p>
</div>
'''

@app.route("/")
def home():
    return render_template_string(BASE_HTML, content=HOME_HTML)

@app.route("/chat")
def chat():
    return render_template_string(BASE_HTML, content=CHAT_HTML)

@app.route("/settings")
def settings():
    return render_template_string(BASE_HTML, content=SETTING_HTML
