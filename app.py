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
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()
        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = user["username"]
                session["role"] = user["role"]
                if user["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                else:
                    return redirect(url_for("user_dashboard"))
        return render_template("login.html", fejl="Forkert brugernavn eller adgangskode.")
    return render_template("login.html")

@app.route("/user")
def user_dashboard():
    if "user" in session and session.get("role") == "bruger":
        return render_template("user_dashboard.html", username=session["user"])
    return redirect(url_for("login"))

@app.route("/admin")
def admin_dashboard():
    if "user" in session and session.get("role") == "admin":
        return render_template("admin_dashboard.html", username=session["user"])
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("profile.html", username=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
