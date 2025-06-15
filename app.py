# Entry point for Navoras v0.1
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Velkommen til Navoras v0.1 – Testversion med login!'

if __name__ == '__main__':
    app.run()