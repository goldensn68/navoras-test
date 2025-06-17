from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'hemmelig-nøgle'
DATABASE = 'navoras.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    role = session['role']
    db = get_db()
    if role == 'admin':
        users = db.execute('SELECT id, email, role FROM users').fetchall()
        return render_template('admin_dashboard.html', users=users)
    else:
        user_id = session['user_id']
        boat = db.execute('SELECT * FROM boats WHERE user_id = ?', (user_id,)).fetchone()
        logs = db.execute('SELECT * FROM logbooks WHERE user_id = ?', (user_id,)).fetchall()
        tasks = db.execute('SELECT * FROM maintenance WHERE user_id = ?', (user_id,)).fetchall()
        return render_template('user_dashboard.html', boat=boat, logs=logs, tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        email = request.form['email']
        password = request.form['password']
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        if user:
            session['user'] = user['email']
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('index'))
        return render_template('login.html', error="Forkert login")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if 'role' in session and session['role'] == 'admin':
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']
            db = get_db()
            db.execute('INSERT INTO users (email, password, role) VALUES (?, ?, ?)', (email, password, role))
            db.commit()
            return redirect(url_for('index'))
        return render_template('register_user.html')
    return redirect(url_for('login'))

@app.route('/add_boat', methods=['POST'])
def add_boat():
    if 'user_id' in session:
        user_id = session['user_id']
        name = request.form['name']
        length = request.form['length']
        motor = request.form['motor']
        db = get_db()
        db.execute('INSERT INTO boats (user_id, name, length, motor) VALUES (?, ?, ?, ?)', (user_id, name, length, motor))
        db.commit()
    return redirect(url_for('index'))

@app.route('/add_logbook', methods=['POST'])
def add_logbook():
    if 'user_id' in session:
        user_id = session['user_id']
        entry = request.form['entry']
        db = get_db()
        db.execute('INSERT INTO logbooks (user_id, entry) VALUES (?, ?)', (user_id, entry))
        db.commit()
    return redirect(url_for('index'))

@app.route('/add_maintenance', methods=['POST'])
def add_maintenance():
    if 'user_id' in session:
        user_id = session['user_id']
        task = request.form['task']
        status = request.form['status']
        db = get_db()
        db.execute('INSERT INTO maintenance (user_id, task, status) VALUES (?, ?, ?)', (user_id, task, status))
        db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
