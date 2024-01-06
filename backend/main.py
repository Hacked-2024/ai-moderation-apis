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

@app.route("/moderate", methods=['POST'])
def moderate():
    data = request.get_json()

    if 'textInput' not in data:
        return "Post request missing correct body keys", 400
    
    input = data["textInput"]
    
    response = client.moderations.create(input=input)
    result = response.results[0]
    output = result.model_dump_json()

    return output, 200


@app.route("/fact-check", methods=['POST'])
def fact_check():
    data = request.get_json()

    if 'textInput' not in data:
        return "Post request missing correct body keys", 400
    
    textInput = data["textInput"]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {
                "role": "user", 
                "content": f"""Assume you are a bot trained to detect misinformation. 
                Output only 1 number on a scale from 1-10, 10 being fact and 1 being a lie.:\"{textInput}\""""
            }
        ]
    )

    result = completion.choices[0].message.content

    return {
        "truthfulness": completion.choices[0].message.content
    }, 200