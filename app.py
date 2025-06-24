from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

# Indlæs brugere fra users.json i roden
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
        return render_template("user_dashboard.html", username=session["username"], boat=None, logs=[], tasks=[])
    return redirect(url_for("login"))

@app.route("/admin")
def admin_dashboard():
    if "username" in session and session.get("role") == "admin":
        # Indlæs brugere og konverter til dict med brugernavn som key
        brugere = load_users()
        users_dict = {bruger["username"]: bruger for bruger in brugere}
        return render_template("admin_dashboard.html", username=session["username"], users=users_dict)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "username" in session:
        return render_template("profile.html", username=session["username"])
    return redirect(url_for("login"))

# Portopsætning til Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
