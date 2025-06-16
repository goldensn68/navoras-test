from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "test" and password == "test":
            return "<h1>Login successful!</h1>"
        return "<h1>Login failed</h1>"
    return '''
        <form method="post">
            <label>Brugernavn: <input type="text" name="username"></label><br>
            <label>Kodeord: <input type="password" name="password"></label><br>
            <input type="submit" value="Log ind">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)