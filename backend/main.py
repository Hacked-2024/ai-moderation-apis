from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin


@app.route("/")
def hello_world():
    return {'data': 'This is the default return content'}