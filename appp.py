from flask import Flask, request, redirect, render_template_string
import datetime
import cv2

app = Flask(__name__)

students = []
phone_count = 0
head_count = 0
face_count = 0

# ---------------- LOGIN PAGE ----------------
login_page = """
<html>
<body style="text-align:center">

<h2>AI Exam Login</h2>

<form action="/login" method="post">
<input name="name" placeholder="Enter Name" required><br><br>
<button type="submit">Start Exam</button>
</form>

</body>
</html>
"""

# ---------------- RULES PAGE ----------------
rules_page = """
<html>
<body style="text-align:center">

<h2>Exam Rules</h2>

<p>No mobile phone</p>
<p>Only one person</p>
<p>No head movement</p>

<button onclick="start()">Accept</button>

<script>
function start(){
window.location="/camera"
}
</script>

</body>
</html>
"""

# ---------------- CAMERA PAGE ----------------
camera_page = """
<html>
<body style="text-align:center">

<h2>Live Exam</h2>

<video id="video" width="500" autoplay></video>

<br><br>

<button onclick="send('phone')">Phone</button>
<button onclick="send('head')">Head</button>
<button onclick="send('face')">Multiple Face</button>

<br><br>

<a href="/dashboard">Go Dashboard</a>

<script>

navigator.mediaDevices.getUserMedia({video:true})
.then(function(stream){
document.getElementById("video").srcObject = stream;
});

function send(type){

fetch("/malpractice",{
method:"POST",
headers:{"Content-Type":"application/x-www-form-urlencoded"},
body:"type="+type
})

alert(type + " detected")

}

</script>

</body>
</html>
"""

# ---------------- DASHBOARD ----------------
dashboard_page = """
<html>
<body style="text-align:center">

<h1>Admin Dashboard</h1>

<h3>Total Students: {{total}}</h3>

<h3>Phone: {{phone}}</h3>
<h3>Head: {{head}}</h3>
<h3>Multiple Faces: {{face}}</h3>

<hr>

{% for s in students %}
<p>{{s}}</p>
{% endfor %}

</body>
</html>
"""

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template_string(login_page)

@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    students.append(name)
    return redirect("/rules")

@app.route("/rules")
def rules():
    return render_template_string(rules_page)

@app.route("/camera")
def camera():
    return render_template_string(camera_page)

@app.route("/malpractice", methods=["POST"])
def malpractice():
    global phone_count, head_count, face_count

    t = request.form["type"]

    if t == "phone":
        phone_count += 1
    elif t == "head":
        head_count += 1
    elif t == "face":
        face_count += 1

    return "ok"

@app.route("/dashboard")
def dashboard():
    return render_template_string(
        dashboard_page,
        total=len(students),
        phone=phone_count,
        head=head_count,
        face=face_count,
        students=students
    )

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)