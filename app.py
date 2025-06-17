from flask import Flask, render_template, redirect, request, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'hemmelig-nøgle'

users = {
    "bruger1@navoras.dk": {"password": "Test1234!", "role": "user"},
    "admin@navoras.dk": {"password": "Admin1234!", "role": "admin"}
}

@app.route('/')
def index():
    if 'user' in session:
        if session['role'] == 'admin':
            return render_template('admin_dashboard.html', user=session['user'])
        return render_template('user_dashboard.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = email
            session['role'] = user['role']
            return redirect(url_for('index'))
        return render_template('login.html', error="Forkert login")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
