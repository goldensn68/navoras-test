from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

# Brug korrekt sti til users.json i roden
def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)["users"]

def save_users(users):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, indent=2, ensure_ascii=False)

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

@app.route("/dashboard")
def user_dashboard():
    if "username" in session and session.get("role") == "bruger":
        return render_template("user_dashboard.html", username=session["username"])
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    if "username" in session and session.get("role") == "admin":
        users = load_users()
        user_dict = {u["username"]: u for u in users}
        return render_template("admin_dashboard.html", username=session["username"], users=user_dict)
    return redirect(url_for("login"))

@app.route("/register_user", methods=["POST"])
def register_user():
    if "username" in session and session.get("role") == "admin":
        new_user = {
            "username": request.form["username"],
            "password": request.form["password"],
            "role": request.form["role"]
        }
        users = load_users()
        users.append(new_user)
        save_users(users)
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "username" in session:
        username = session["username"]
        role = session.get("role", "bruger")
        # Midlertidige testdata – disse kan senere gøres dynamiske
        points = 42
        badges = ["Motorpasser", "Logbogsfører", "Feedbackgiver"]
        return render_template("profile.html", username=username, role=role, points=points, badges=badges)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Portopsætning til Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
