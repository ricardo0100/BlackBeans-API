import os
import urllib.request

from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template("index.html", menuActive="index")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
