
from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        brugernavn = request.form["brugernavn"]
        adgangskode = request.form["adgangskode"]
        if brugernavn.lower() == "admin" and adgangskode == "admin123":
            session["user"] = "admin"
            return redirect(url_for("dashboard_admin"))
        elif brugernavn.lower() == "bruger1" and adgangskode == "test123":
            session["user"] = "bruger1"
            return redirect(url_for("dashboard_user"))
        else:
            return "Forkert brugernavn eller adgangskode", 400
    return render_template("login.html")

@app.route("/dashboard_admin")
def dashboard_admin():
    if session.get("user") != "admin":
        return redirect(url_for("login"))
    return render_template("dashboard_admin.html", bruger="admin")

@app.route("/dashboard_user")
def dashboard_user():
    if session.get("user") != "bruger1":
        return redirect(url_for("login"))
    return render_template("dashboard_user.html", bruger="bruger1")

@app.route("/logud")
def logud():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
