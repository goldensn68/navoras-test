from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Navoras v0.1 testside kører!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
