from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=7)

# Dummy-brugere til test
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'bruger2': {'password': 'test123', 'role': 'user'}
}

# Dummydata til bruger-dashboard
dummy_boats = {
    'bruger2': {'name': 'Testbåd', 'length': '30 fod', 'motor': 'Volvo Penta'}
}

dummy_logs = {
    'bruger2': [{'entry': 'Tog ud og fiskede i 3 timer.'}]
}

dummy_tasks = {
    'bruger2': [{'task': 'Olieskift', 'status': 'Udført'}]
}

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session.permanent = True
            session['user'] = username
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Forkert brugernavn eller adgangskode.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    username = session['user']
    role = session.get('role')

    if role == 'admin':
        return render_template('admin_dashboard.html', users=users)
    else:
        boat = dummy_boats.get(username)
        logs = dummy_logs.get(username, [])
        tasks = dummy_tasks.get(username, [])
        return render_template('user_dashboard.html', boat=boat, logs=logs, tasks=tasks)

@app.route('/register_user', methods=['POST'])
def register_user():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    if username not in users:
        users[username] = {'password': password, 'role': role}
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dette er vigtigt for Render!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

