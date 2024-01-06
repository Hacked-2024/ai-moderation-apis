from flask import Flask, request, render_template, Response
from flask_cors import CORS, cross_origin

from dotenv import load_dotenv
import os

load_dotenv("./.env")

from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPEN_API_KEY")
)

@app.route("/")
def hello_world():
    return {'data': 'This is the default return content'}

@app.route("/moderate-open-ai", methods=['POST'])
def moderate_open_ai():
    data = request.get_json()

    if 'textInput' not in data:
        return "Posted data missing key(s)", 400
    
    input = data["textInput"]
    
    response = client.moderations.create(input=input)
    output = response.results[0]

    return {
        "output": output
    }
    

