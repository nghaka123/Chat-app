from flask import Flask, render_template_string, request, jsonify, redirect
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
.nav{text-align:center; margin-bottom:15px}
.nav a{margin:0 10px; text-decoration:none; color:#007bff; font-weight:bold}
h2{text-align:center; color:#333}
#chat{border:1px solid #ccc; height:350px; overflow-y:scroll; padding:10px; background:white; margin-bottom:10px; border-radius:8px}
#input-box{display:flex; flex-direction:column; gap:10px}
.input-row{display:flex; gap:10px}
input{flex:1; padding:12px; border:1px solid #ccc; border-radius:5px}
button{padding:12px 20px; background:#007bff; color:white; border:none; border-radius:5px; cursor:pointer}
button:hover{background:#0056b3}
p{margin:5px 0; padding:10px; border-radius:10px; max-width:70%}
.me{background:#d1e7ff; margin-left:auto; text-align:right}
.other{background:#e9ecef; margin-right:auto; text-align:left}
b{color:#004085}
.setting-box{background:white; padding:20px; border-radius:8px}
</style>
</head>
<body>
<div class="nav">
<a href="/">Chat</a> | <a href="/settings">Settings</a>
</div>
{{content}}
</body>
</html>
'''

CHAT_HTML = '''
<h2>Ka Chat App - Live Chat</h2>
<div id="chat"></div>
<div id="input-box">
<div class="input-row">
<input id="name" placeholder="I hming ziak rawh" required style="width:120px; flex:0.3">
<input id="msg" placeholder="Thu ziak rawh..." autocomplete="off" required>
</div>
<button onclick="send()">Thawn</button>
</div>

<script>
let myName = localStorage.getItem("myName") || "";
let myColor = localStorage.getItem("myColor") || "#d1e7ff";

function loadMessages(){
  fetch('/messages').then(r=>r.json()).then(data=>{
    let chat = document.getElementById("chat");
    chat.inner
