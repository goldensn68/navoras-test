
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_users():
    with open('users.json') as f:
        return json.load(f)

def load_logbook():
    with open('logbook.json') as f:
        return json.load(f)

def save_logbook(data):
    with open('logbook.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('user_dashboard', username=username))
        error = 'Forkert brugernavn eller adgangskode.'
    return render_template('login.html', error=error)

@app.route('/dashboard/<username>')
def user_dashboard(username):
    logbook = load_logbook()
    user_entries = [entry for entry in logbook if entry['username'] == username]
    return render_template('user_dashboard.html', username=username, logbook=user_entries)

@app.route('/edit_log/<int:entry_id>', methods=['GET', 'POST'])
def edit_log(entry_id):
    logbook = load_logbook()
    entry = next((e for e in logbook if e['id'] == entry_id), None)
    if request.method == 'POST':
        entry['title'] = request.form['title']
        entry['content'] = request.form['content']
        save_logbook(logbook)
        return redirect(url_for('user_dashboard', username=entry['username']))
    return render_template('edit_log.html', entry=entry)

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
