
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
