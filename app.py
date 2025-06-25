from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'navoras_secret'

USER_FILE = 'users.json'
LOG_FILE = 'log.json'

def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, 'r') as f:
        return json.load(f)

def save_logs(logs):
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['user'] = username
            return redirect('/user/dashboard')
        else:
            return 'Forkert login'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/user/dashboard')
def user_dashboard():
    if 'user' not in session:
        return redirect('/login')
    logs = load_logs()
    user_logs = [log for log in logs if log['user'] == session['user']]
    return render_template('user_dashboard.html', logs=user_logs)

@app.route('/edit_log/<int:log_id>', methods=['GET', 'POST'])
def edit_log(log_id):
    if 'user' not in session:
        return redirect('/login')
    logs = load_logs()
    log = logs[log_id]
    if request.method == 'POST':
        updated_text = request.form['entry']
        logs[log_id]['entry'] = updated_text
        save_logs(logs)
        return redirect('/user/dashboard')
    return render_template('edit_log.html', log=log, log_id=log_id)
