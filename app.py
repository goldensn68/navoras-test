from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

# Hjælpefunktioner
def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)["users"]

def load_boat_data():
    if os.path.exists("boat_data.json"):
        with open("boat_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_boat_data(data):
    with open("boat_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_log_entries():
    if os.path.exists("log_entries.json"):
        with open("log_entries.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_log_entries(entries):
    with open("log_entries.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

# Ruter
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

@app.route("/dashboard")
def user_dashboard():
    if "username" not in session or session.get("role") != "bruger":
        return redirect(url_for("login"))
    boat_data = load_boat_data()
    user_boat = boat_data.get(session["username"], {})
    log_entries = load_log_entries()
    return render_template("user_dashboard.html", boat=user_boat, logs=log_entries, username=session["username"])

@app.route("/edit_boat", methods=["GET", "POST"])
def edit_boat():
    if "username" not in session or session.get("role") != "bruger":
        return redirect(url_for("login"))
    boat_data = load_boat_data()
    if request.method == "POST":
        navn = request.form.get("name")
        længde = request.form.get("length")
        motor = request.form.get("motor")
        boat_data[session["username"]] = {"name": navn, "length": længde, "motor": motor}
        save_boat_data(boat_data)
        return redirect(url_for("user_dashboard"))
    user_boat = boat_data.get(session["username"], {})
    return render_template("edit_boat.html", boat=user_boat)

@app.route("/add_log", methods=["GET", "POST"])
def add_log():
    if "username" not in session or session.get("role") != "bruger":
        return redirect(url_for("login"))
    if request.method == "POST":
        entry = request.form.get("entry")
        if entry:
            entries = load_log_entries()
            entries.append({"entry": entry, "user": session["username"]})
            save_log_entries(entries)
        return redirect(url_for("user_dashboard"))
    return render_template("add_log_entry.html")

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("profile.html", username=session["username"])

@app.route("/admin")
def admin_dashboard():
    if "username" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    brugere = load_users()
    return render_template("admin_dashboard.html", users={u["username"]: u for u in brugere})

# Portopsætning til Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
