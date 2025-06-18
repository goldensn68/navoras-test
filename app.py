
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Navoras v0.1 Testside'

@app.route('/test')
def test():
    return 'Testside kører korrekt.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
