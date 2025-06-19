# Navoras Test App - Flask version
from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'user':
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

