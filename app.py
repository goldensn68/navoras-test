
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

logbog = []
opgaver = []
boat_info = {"navn": "", "motor": ""}

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        brugernavn = request.form["username"]
        adgangskode = request.form["password"]
        if brugernavn == "Admin" and adgangskode == "admin123":
            session["rolle"] = "admin"
            return redirect("/dashboard_admin")
        elif brugernavn == "Bruger1" and adgangskode == "test123":
            session["rolle"] = "bruger"
            return redirect("/dashboard")
        else:
            return "Forkert login"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if session.get("rolle") == "bruger":
        return render_template("dashboard_user.html")
    return redirect("/login")

@app.route("/dashboard_admin")
def dashboard_admin():
    if session.get("rolle") == "admin":
        return render_template("dashboard_admin.html")
    return redirect("/login")

@app.route("/boat", methods=["GET", "POST"])
def boat():
    if request.method == "POST":
        boat_info["navn"] = request.form["navn"]
        boat_info["motor"] = request.form["motor"]
    return render_template("boat.html", navn=boat_info["navn"], motor=boat_info["motor"])

@app.route("/logbook", methods=["GET", "POST"])
def logbook():
    if request.method == "POST":
        entry = {"titel": request.form["titel"], "tekst": request.form["tekst"]}
        logbog.append(entry)
    return render_template("logbook.html", logbog=logbog)

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        opgave = {"titel": request.form["titel"], "kategori": request.form["kategori"]}
        opgaver.append(opgave)
    return render_template("tasks.html", opgaver=opgaver)

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if session.get("rolle") != "bruger":
        return redirect("/dashboard_admin")
    return render_template("feedback.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
