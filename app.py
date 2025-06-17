from flask import Flask, render_template, redirect, request, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'hemmelig-nøgle'

dummy_user = {
    "email": "bruger1@navoras.dk",
    "password": "Test1234!"
}

@app.route('/')
def index():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == dummy_user['email'] and password == dummy_user['password']:
            session['user'] = email
            return redirect(url_for('index'))
        return render_template('login.html', error="Forkert login")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
