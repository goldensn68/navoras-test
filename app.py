from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = 'hemmelig_nøgle'

def load_users():
    with open('users.json', encoding='utf-8') as f:
        return json.load(f)['users']

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        brugernavn = request.form["username"]
        kodeord = request.form["password"]
        brugere = load_users()
        for bruger in brugere:
            if bruger["username"] == brugernavn and bruger["password"] == kodeord:
                session["username"] = brugernavn
                session["role"] = bruger.get("role", "user")
                if session["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                else:
                    return redirect(url_for("user_dashboard"))
        return render_template("login.html", fejl="Forkert brugernavn eller adgangskode.")
    return render_template("login.html")

@app.route("/dashboard")
def user_dashboard():
    if "username" in session and session.get("role") == "user":
        logs = [{"entry": "Skiftet olie"}, {"entry": "Renset vandtank"}]
        tasks = [{"task": "Tjek sejl", "status": "Afventer"}, {"task": "Skift zinkanoder", "status": "Udført"}]
        badges = ["Motorpasser", "Maskinist"]
        return render_template("user_dashboard.html", logs=logs, tasks=tasks, badges=badges)
    return redirect(url_for("login"))

@app.route("/admin")
def admin_dashboard():
    if "username" in session and session.get("role") == "admin":
        brugere = load_users()
        user_dict = {b['username']: {"role": b["role"]} for b in brugere}
        return render_template("admin_dashboard.html", users=user_dict)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "username" in session:
        badges = ["Motorpasser", "Maskinist"]
        points = 120
        return render_template("profile.html", badges=badges, points=points)
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)