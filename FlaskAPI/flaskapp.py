from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    print('hit the func')
    return "Success!"