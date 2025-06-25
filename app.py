
from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)["users"]

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        brugernavn = request.form["username"]
        kodeord = request.form["password"]
        brugere = load_users()
        for bruger in brugere:
            if bruger["username"] == brugernavn and bruger["password"] == kodeord:
                session["username"] = brugernavn
                session["role"] = bruger.get("role", "bruger")
                if session["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                else:
                    return redirect(url_for("user_dashboard"))
        return render_template("login.html", fejl="Forkert brugernavn eller adgangskode.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin")
def admin_dashboard():
    if "username" in session and session.get("role") == "admin":
        return render_template("admin_dashboard.html", username=session["username"])
    return redirect(url_for("login"))

@app.route("/dashboard")
def user_dashboard():
    if "username" in session and session.get("role") == "bruger":
        logs = [{"entry": "Testsejlads til Ærø – alt ok"}]
        tasks = [{"task": "Skift motorolie", "status": "Udført"}]
        boat = {"name": "M/S Test", "length": "10m", "motor": "Yanmar 30HK"}
        return render_template("user_dashboard.html", username=session["username"], logs=logs, tasks=tasks, boat=boat)
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    return render_template("profile.html", username=username, points=50, badges=["Ny Sejler", "Vedligeholder"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
