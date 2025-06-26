
from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        brugernavn = request.form["brugernavn"]
        adgangskode = request.form["adgangskode"]
        if brugernavn == "Bruger1" and adgangskode == "test123":
            session["user"] = brugernavn
            session["rolle"] = "bruger"
            return redirect("/bruger_dashboard")
        elif brugernavn == "Admin" and adgangskode == "admin123":
            session["user"] = brugernavn
            session["rolle"] = "admin"
            return redirect("/admin_dashboard")
        else:
            return "Forkert brugernavn eller adgangskode"
    return render_template("login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if "user" not in session or session.get("rolle") != "admin":
        return redirect("/login")
    return render_template("admin_dashboard.html", bruger=session["user"])

@app.route("/bruger_dashboard")
def bruger_dashboard():
    if "user" not in session or session.get("rolle") != "bruger":
        return redirect("/login")
    return render_template("bruger_dashboard.html", bruger=session["user"])

@app.route("/rediger_baad", methods=["GET", "POST"])
def rediger_baad():
    if "user" not in session:
        return redirect("/login")
    if request.method == "POST":
        session["boat"] = {
            "navn": request.form["baadnavn"],
            "motor": request.form["motorinfo"]
        }
        return redirect("/bruger_dashboard")
    return render_template("rediger_baad.html")

@app.route("/logbog", methods=["GET", "POST"])
def logbog():
    if "user" not in session:
        return redirect("/login")
    if "logbog" not in session:
        session["logbog"] = []
    if request.method == "POST":
        indlaeg = {
            "titel": request.form["titel"],
            "beskrivelse": request.form["beskrivelse"]
        }
        session["logbog"].append(indlaeg)
    return render_template("logbog.html", logbog=session.get("logbog", []))

@app.route("/vedligehold", methods=["GET", "POST"])
def vedligehold():
    if "user" not in session:
        return redirect("/login")
    if "opgaver" not in session:
        session["opgaver"] = []
    if request.method == "POST":
        opgave = {
            "titel": request.form["titel"],
            "kategori": request.form["kategori"]
        }
        session["opgaver"].append(opgave)
    return render_template("vedligehold.html", opgaver=session.get("opgaver", []))

@app.route("/oversigt")
def oversigt():
    if "user" not in session:
        return redirect("/login")
    boat = session.get("boat", {"navn": "Ikke angivet", "motor": "Ikke angivet"})
    logbog = session.get("logbog", [])
    opgaver = session.get("opgaver", [])
    return render_template("oversigt.html", boat=boat, logbog=logbog, opgaver=opgaver)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
