from flask import Flask
from flask import render_template
from spo2yt import Spo2yt

app = Flask(__name__)

my_app = Spo2yt()

@app.route("/")
def index():
    return render_template('index.html')
