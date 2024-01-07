import requests
import json
import base64

API_TOKEN = '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'
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

    for model_id in MODEL_IDS:
        results = query(model_id, image_data)
        print(results)
        score = results[0]['score'] if results[0]['label'] == 'hateful' else results[1]['score']
        if score <= 0.5: return False

    return True


if __name__ == '__main__':
    filename = "./pride_burn.png"
    with open(filename, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    print(classify_image(image_data))