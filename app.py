from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'hemmelig_nøgle'

DATA_PATH = 'data/users.json'

# Hent brugerdata
def load_users():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# Gem brugerdata
def save_users(users):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        kodeord = request.form['kodeord']
        users = load_users()

        for brugernavn, brugerdata in users.items():
            if brugerdata['email'] == email and brugerdata['kodeord'] == kodeord:
                session['brugernavn'] = brugernavn
                session['rolle'] = brugerdata.get('rolle', 'bruger')
                return redirect(url_for('dashboard'))

        error = 'Ugyldig e-mail eller adgangskode'

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'brugernavn' not in session:
        return redirect(url_for('login'))
    
    brugernavn = session['brugernavn']
    rolle = session.get('rolle', 'bruger')

    if rolle == 'admin':
        return render_template('admin_dashboard.html', brugernavn=brugernavn)
    else:
        return render_template('dashboard.html', brugernavn=brugernavn)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Sørg for at binde korrekt til port, som Render stiller til rådighed
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
