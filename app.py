
from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'hemmelig_noegle'

# Dummy data
brugere = {
    "Bruger1": {"adgangskode": "test123", "rolle": "bruger"},
    "Admin": {"adgangskode": "admin123", "rolle": "admin"}
}

@app.route("/", methods=["GET"])
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        brugernavn = request.form["brugernavn"]
        adgangskode = request.form["adgangskode"]
        bruger = brugere.get(brugernavn)
        if bruger and bruger["adgangskode"] == adgangskode:
            session["user"] = brugernavn
            session["rolle"] = bruger["rolle"]
            if bruger["rolle"] == "admin":
                return redirect("/admin_dashboard")
            else:
                return redirect("/bruger_dashboard")
        return render_template("login.html", fejl="Forkert brugernavn eller adgangskode")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("rolle") != "admin":
        return redirect("/login")
    return render_template("admin_dashboard.html", bruger=session["user"])

@app.route("/bruger_dashboard")
def bruger_dashboard():
    if session.get("rolle") != "bruger":
        return redirect("/login")
    return render_template("bruger_dashboard.html", bruger=session["user"])

@app.route("/min_baad")
def min_baad():
    if "user" not in session:
        return redirect("/login")
    return render_template("min_baad.html")

@app.route("/logbog")
def logbog():
    if "user" not in session:
        return redirect("/login")
    return render_template("logbog.html")

@app.route("/vedligehold")
def vedligehold():
    if "user" not in session:
        return redirect("/login")
    return render_template("vedligehold.html")

@app.route("/oversigt")
def oversigt():
    if "user" not in session:
        return redirect("/login")
    return render_template("oversigt.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
