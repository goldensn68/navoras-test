
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

# Dummy login-data
brugere = {
    "Bruger1": {"kode": "test123", "rolle": "bruger"},
    "Admin": {"kode": "admin123", "rolle": "admin"}
}

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        brugernavn = request.form.get("brugernavn")
        kode = request.form.get("kode")
        bruger = brugere.get(brugernavn)
        if bruger and bruger["kode"] == kode:
            session["user"] = brugernavn
            session["rolle"] = bruger["rolle"]
            if bruger["rolle"] == "admin":
                return redirect("/admin_dashboard")
            return redirect("/bruger_dashboard")
        else:
            return render_template("login.html", fejl="Forkert brugernavn eller adgangskode.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/bruger_dashboard")
def bruger_dashboard():
    if session.get("rolle") != "bruger":
        return redirect("/login")
    return render_template("bruger_dashboard.html", bruger=session.get("user"))

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("rolle") != "admin":
        return redirect("/login")
    return render_template("admin_dashboard.html", admin=session.get("user"))

@app.route("/min_baad")
def min_baad():
    return render_template("min_baad.html")

@app.route("/logbog")
def logbog():
    return render_template("logbog.html")

@app.route("/vedligehold")
def vedligehold():
    return render_template("vedligehold.html")

@app.route("/oversigt")
def oversigt():
    return render_template("oversigt.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
