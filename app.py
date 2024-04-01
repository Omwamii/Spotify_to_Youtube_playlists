from flask import Flask
from flask import render_template
from app_class import App

app = Flask(__name__)
youtube = App()

@app.route("/")
def index():
    return render_template('index.html')
