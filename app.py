from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "test" and password == "test":
            session["user"] = username
            return redirect(url_for("dashboard"))
        return "Login mislykkedes"
    return '''
        <form method="post">
            <h2>Login</h2>
            <input type="text" name="username" placeholder="Brugernavn"><br>
            <input type="password" name="password" placeholder="Kodeord"><br>
            <button type="submit">Log ind</button>
        </form>
    '''

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f'''
        <h1>Velkommen, {session["user"]}</h1>
        <ul>
            <li><a href="/boat">Bådinformation</a></li>
            <li><a href="/maintenance">Vedligeholdelse</a></li>
            <li><a href="/logbook">Logbog</a></li>
            <li><a href="/logout">Log ud</a></li>
        </ul>
    '''

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/boat")
def boat():
    return "<h2>Dummy bådinformation</h2>"

@app.route("/maintenance")
def maintenance():
    return "<h2>Dummy vedligeholdelsesoversigt</h2>"

@app.route("/logbook")
def logbook():
    return "<h2>Dummy logbog</h2>"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)