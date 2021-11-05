from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return f"<h1>ホーム</h1>"

@app.route('/<drink>')
def hello(drink):
    return f"<h1>好きな飲み物は{drink}</h1>"