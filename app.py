from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)["users"]

def save_users(users):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, ensure_ascii=False, indent=2)

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
                session["role"] = bruger.get("role", "user")
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

@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    users = {user['username']: user for user in load_users()}
    return render_template("admin_dashboard.html", users=users)

@app.route("/register_user", methods=["POST"])
def register_user():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    users = load_users()
    new_user = {
        "username": request.form["username"],
        "password": request.form["password"],
        "role": request.form["role"]
    }
    users.append(new_user)
    save_users(users)
    return redirect(url_for("admin_dashboard"))

@app.route("/dashboard")
def user_dashboard():
    if "username" not in session or session.get("role") != "user":
        return redirect(url_for("login"))
    return render_template("user_dashboard.html", username=session["username"], points=120, badges=["Aktiv Bruger", "Vedligeholdelsesmester"])

if __name__ == "__main__":
    app.run(debug=True)
