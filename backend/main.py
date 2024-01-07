import base64
import image

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

MAX_OPENAI_CALLS = 50

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

@app.route("/filter-check", methods=['POST'])
def filter_check():
    data = request.get_json()

    if 'textInput' not in data or 'filter' not in data:
        return "Post request missing correct body keys", 400
    
    textInput = data["textInput"]
    filter = data["filter"]

    response = getNumericalPromptResponse(
        f"""Assume you are a bot trained to detect hate speech and harmful content. Does this message, \"{textInput}\", contain hate speech or harmful content in any of these catrgories: {filter}? return 1 if True or 0 if False."""
    )

    return {
        "filtered": response
    }, 200


@app.route("/fact-check", methods=['POST'])
def fact_check():
    data = request.get_json()

    if 'textInput' not in data:
        return "Post request missing correct body keys", 400
    
    textInput = data["textInput"]

    response = getNumericalPromptResponse(
        f"""Assume you are a bot trained to detect misinformation on social media captions. 
        Output only one number on a scale from 1-10, 1 being fact and 10 being a lie. If the input is opinionated, lower the final score by 2, unless the input offers medical advice/information. Input: \"{textInput}\""""

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
                Output only one number on a scale from 1-10, 10 being extemely offensive and 1 being inoffensive.:\"{textInput}\""""
    )

    return {
        "offensiveness": response
    }, 200

@app.route("/hateful-image", methods=['POST'])
def hateful_image():
    """
    Decides whether an image contains hateful content.
    Make sure the body is in JSON format.

    method: POST
    fields:
        image: a 64base encoding of an image

    Responses:
        200:
            fields:
                hateful: true if hateful, false if not
        
        400:
            Reason: image field wasn't passed or was passed incorrectly
            Reason: image field is not encoded in base64
        
        503:
            Reason: Models are not running. Maybe they'll work later.
    """
    data = request.get_json()

    if "image" not in data:
        return "Post request missing correct body keys", 400

    image_data = data["image"]

    # Not working for now, maybe fix later
    # if base64.b64encode(base64.b64decode(image_data)) != image_data:
    #     return "image_data not in base64", 400

    hateful = image.classify_image(image_data)
    if isinstance(hateful, str): return "Model warming up :(", 503

    return {
        "hateful": hateful
    }, 200