from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = '''
<!doctype html>
<html>
<head><title>Ka Chat App</title>
<style>
body{font-family:Arial; padding:20px; background:#f0f0f0}
#chat{border:1px solid #ccc; height:400px; overflow-y:scroll; padding:10px; background:white; margin-bottom:10px}
input{width:80%; padding:10px}
button{padding:10px 20px}
</style>
</head>
<body>
<h2>Ka Chat App</h2>
<div id="chat"></div>
<input id="msg" placeholder="Thu ziak rawh...">
<button onclick="send()">Thawn</button>

<script>
function send(){
  let m = document.getElementById("msg").value;
  if(m){
    document.getElementById("chat").innerHTML += "<p><b>Nang:</b> "+m+"</p>";
    document.getElementById("msg").value = "";
  }
}
</script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
