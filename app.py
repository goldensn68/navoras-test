from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = 'hemmelig_nøgle'

PORT = int(os.environ.get("PORT", 5000))

def load_users():
    with open("users.json") as f:
        return json.load(f)

def load_boats():
    with open("boats.json") as f:
        return json.load(f)

def load_logs():
    with open("logs.json") as f:
        return json.load(f)

def load_tasks():
    with open("tasks.json") as f:
        return json.load(f)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        brugernavn = request.form['brugernavn']
        adgangskode = request.form['adgangskode']
        users = load_users()
        if brugernavn in users and users[brugernavn]['adgangskode'] == adgangskode:
            session['user'] = brugernavn
            session['rolle'] = users[brugernavn]['rolle']
            if users[brugernavn]['rolle'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            return "Forkert brugernavn eller adgangskode"
    return render_template('login.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    boats = load_boats()
    logs = load_logs()
    tasks = load_tasks()
    boat = boats.get(user)
    user_logs = logs.get(user, [])
    user_tasks = tasks.get(user, [])
    return render_template('user_dashboard.html', boat=boat, logs=user_logs, tasks=user_tasks)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' not in session or session.get('rolle') != 'admin':
        return redirect(url_for('login'))
    users = load_users()
    return render_template('admin_dashboard.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=PORT)