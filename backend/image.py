import requests
import json
import base64

API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/yuvalkirstain/PickScore_v1"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename, candidate_labels):

    with open(filename, "rb") as image_file:
        base64_encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Define the payload with the base64-encoded image data and labels for zero-shot classification
    payload = {
        "inputs": base64_encoded_image,
        "parameters": {
            "candidate_labels": ["hateful", "normal"]
        }
    }

    response = requests.post(API_URL, json=payload)

    return json.loads(response.content.decode("utf-8"))
data = query("./eagle.webp", "hateful,normal")

print(data)