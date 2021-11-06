from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<string:drink>')
def drink(drink):
    return f"<h1>好きな飲み物は{drink}</h1>"

@app.route('/<int:number>')
def number(number):
    return f"<h1>好きな正数は{number}</h1>"