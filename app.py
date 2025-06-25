from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

DATA_DIR = "."
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BOAT_FILE = os.path.join(DATA_DIR, "boat.json")
LOGS_FILE = os.path.join(DATA_DIR, "logs.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")

def load_json(file_path, default):
    if not os.path.exists(file_path):
        return default
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        brugernavn = request.form["username"]
        kodeord = request.form["password"]
        brugere = load_json(USERS_FILE, {}).get("users", [])
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
    if "username" not in session or session.get("role") != "bruger":
        return redirect(url_for("login"))
    boat = load_json(BOAT_FILE, {}).get(session["username"])
    logs = load_json(LOGS_FILE, {}).get(session["username"], [])
    tasks = load_json(TASKS_FILE, {}).get(session["username"], [])
    return render_template("user_dashboard.html", boat=boat, logs=logs, tasks=tasks)

@app.route("/admin")
def admin_dashboard():
    if "username" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    users = {u["username"]: u for u in load_json(USERS_FILE, {}).get("users", [])}
    return render_template("admin_dashboard.html", users=users)

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("profile.html", username=session["username"], points=50, badges=["Starter", "Skipper"])

@app.route("/edit_boat", methods=["GET", "POST"])
def edit_boat():
    if "username" not in session:
        return redirect(url_for("login"))
    boats = load_json(BOAT_FILE, {})
    if request.method == "POST":
        boats[session["username"]] = {
            "name": request.form["name"],
            "length": request.form["length"],
            "motor": request.form["motor"]
        }
        save_json(BOAT_FILE, boats)
        return redirect(url_for("user_dashboard"))
    boat = boats.get(session["username"])
    return render_template("edit_boat.html", boat=boat)

@app.route("/add_log", methods=["GET", "POST"])
def add_log():
    if "username" not in session:
        return redirect(url_for("login"))
    logs = load_json(LOGS_FILE, {})
    if request.method == "POST":
        logs.setdefault(session["username"], []).append({
            "entry": request.form["entry"]
        })
        save_json(LOGS_FILE, logs)
        return redirect(url_for("user_dashboard"))
    return render_template("add_log.html")

@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if "username" not in session:
        return redirect(url_for("login"))
    tasks = load_json(TASKS_FILE, {})
    if request.method == "POST":
        tasks.setdefault(session["username"], []).append({
            "task": request.form["task"],
            "status": "Aktiv"
        })
        save_json(TASKS_FILE, tasks)
        return redirect(url_for("user_dashboard"))
    return render_template("add_task.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)