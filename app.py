from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)["users"]

def load_boat():
    with open("boat.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_boat(data):
    with open("boat.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_logs():
    with open("log.json", "r", encoding="utf-8") as f:
        return json.load(f)["logs"]

def save_logs(logs):
    with open("log.json", "w", encoding="utf-8") as f:
        json.dump({"logs": logs}, f, ensure_ascii=False, indent=2)

def load_tasks():
    with open("tasks.json", "r", encoding="utf-8") as f:
        return json.load(f)["tasks"]

def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump({"tasks": tasks}, f, ensure_ascii=False, indent=2)

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

@app.route("/dashboard", methods=["GET", "POST"])
def user_dashboard():
    if "username" in session and session.get("role") == "bruger":
        boat = load_boat()
        logs = load_logs()
        tasks = load_tasks()
        return render_template("user_dashboard.html", boat=boat, logs=logs, tasks=tasks)
    return redirect(url_for("login"))

@app.route("/edit_boat", methods=["GET", "POST"])
def edit_boat():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        boat = {
            "name": request.form["name"],
            "length": request.form["length"],
            "motor": request.form["motor"]
        }
        save_boat(boat)
        return redirect(url_for("user_dashboard"))
    boat = load_boat()
    return render_template("edit_boat.html", boat=boat)

@app.route("/add_log", methods=["POST"])
def add_log():
    if "username" not in session:
        return redirect(url_for("login"))
    new_entry = request.form["entry"]
    logs = load_logs()
    logs.append({"entry": new_entry})
    save_logs(logs)
    return redirect(url_for("user_dashboard"))

@app.route("/add_task", methods=["POST"])
def add_task():
    if "username" not in session:
        return redirect(url_for("login"))
    task_text = request.form["task"]
    tasks = load_tasks()
    tasks.append({"task": task_text, "status": "planlagt"})
    save_tasks(tasks)
    return redirect(url_for("user_dashboard"))

@app.route("/admin")
def admin_dashboard():
    if "username" in session and session.get("role") == "admin":
        brugere = load_users()
        return render_template("admin_dashboard.html", users={u['username']: u for u in brugere})
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
