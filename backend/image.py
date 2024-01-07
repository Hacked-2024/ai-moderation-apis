import requests
import json
import base64
import time

from dotenv import load_dotenv
import os

load_dotenv("./.env")
#Use below env path if running image.py as main
#load_dotenv("./ai-moderation-apis/backend/.env")

API_TOKEN = os.environ.get("API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/"
MODEL_IDS = ["yuvalkirstain/PickScore_v1", "openai/clip-vit-large-patch14", "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"]

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(model_id, image_data):
    payload = {
        "inputs": image_data,
        "parameters": {
            "candidate_labels": ["hateful", "normal"],
        },
        "wait_for_model": True             
    }

    response = requests.post(API_URL + model_id, headers=headers, json=payload)

    return json.loads(response.content.decode("utf-8"))

def classify_image(image_data):
    scores = []
    for model_id in MODEL_IDS:
        for i in range(2):
            results = query(model_id, image_data)
            
            if isinstance(results, list): 
                scores.append(results[0]['score'] if results[0]['label'] == 'hateful' else results[1]['score'])
                break
            
            time.sleep(2)

    if not scores: return "Error"

    hateful = True
    for score in scores: hateful = hateful and (score > 0.5)
    return hateful


if __name__ == '__main__':
    filename = "./pride_burn.png"
    with open(filename, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    print(classify_image(image_data))