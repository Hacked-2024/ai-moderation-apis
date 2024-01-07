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

CORS(app)

MAX_OPENAI_CALLS = 3

def getNumericalPromptResponse(prompt):
    response = ""
    calls = 0
    while not response.isdigit():

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        response = completion.choices[0].message.content

        if not response: 
            response = ""

        calls += 1
        if calls == MAX_OPENAI_CALLS:
            raise ConnectionError("Failed to receive proper OpenAI response")

    return response

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

    response = getNumericalPromptResponse(
        f"""Assume you are a bot trained to detect misinformation. 
                Output only 1 number on a scale from 1-10, 10 being fact and 1 being a lie.:\"{textInput}\""""
    )

    return {
        "truthfulness": response
    }, 200

@app.route("/offensiveness", methods=['POST'])
def offensiveness():
    data = request.get_json()

    if 'textInput' not in data:
        return "Post request missing correct body keys", 400
    
    textInput = data["textInput"]

    response = getNumericalPromptResponse(
        f"""Assume you are a bot trained to detect offensive speech. 
                Output only 1 number on a scale from 1-10, 10 being extemely offensive and 1 being inoffensive.:\"{textInput}\""""
    )

    return {
        "offensiveness": response
    }, 200