# Flask entry point
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Navoras v0.1 kører på Render!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)