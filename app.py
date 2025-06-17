
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login")
def login():
    return "<h1>Login-side (dummy)</h1>"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
