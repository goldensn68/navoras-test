from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

# Brug korrekt sti til users.json i roden
def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)["users"]

@app.route("/")
def index():
    return render_template("index.html")

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

@app.route("/dashboard")
def user_dashboard():
    if "username" in session and session.get("role") == "bruger":
        # Dummydata til båd, log og vedligeholdelse
        boat = {"name": "Havmåge", "length": "8,5 m", "motor": "Yanmar 2GM20"}
        logs = [{"entry": "Sejlede til Anholt"}, {"entry": "Lille tur i fjorden"}]
        tasks = [{"task": "Olieskift", "status": "Afsluttet"}, {"task": "Filtertjek", "status": "Afventer"}]

        return render_template("user_dashboard.html",
                               username=session["username"],
                               boat=boat,
                               logs=logs,
                               tasks=tasks)
    return redirect(url_for("login"))

@app.route("/admin")
def admin_dashboard():
    if "username" in session and session.get("role") == "admin":
        users = {user["username"]: user for user in load_users()}
        return render_template("admin_dashboard.html", username=session["username"], users=users)
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))

    # Dummydata til visning
    badges = ["Motorpasser", "Logbogssejler"]
    points = 75
    strike_days = 12

    return render_template("profile.html",
                           username=session["username"],
                           badges=badges,
                           points=points,
                           strike_days=strike_days)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Portopsætning til Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
