from flask import Flask, render_template, request, redirect
import datetime
import csv

app = Flask(__name__)

TOTAL_CANDIDATES = 30
current_students = 0
malpractice_count = 0

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/enter", methods=["POST"])
def enter_exam():

    global current_students

    name = request.form["name"]
    login_time = datetime.datetime.now()

    current_students += 1

    with open("exam_log.csv","a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name,"LOGIN",login_time])

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        total=TOTAL_CANDIDATES,
        current=current_students,
        malpractice=malpractice_count
    )

if __name__ == "__main__":
    app.run(debug=True)