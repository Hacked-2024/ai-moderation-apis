## My-Five-Tender-Toesies presents:
# Tweezer API
This Api uses AI models to classify text and image media as hateful, harmful, and misinformation.
It's intended use is for social media identification. See our [front end implementation](https://github.com/my-five-tender-toesies/tweezer) and our [demo](https://github.com/my-five-tender-toesies/tweezer-social-media).

## Endpoints

The following endpoints below must be called with a POST, containing the field "textInput" which holds text to be classified.
### /filter-check
Checks if the given text is hateful or harmful content. Returns 1 if hateful content was found, 0 otherwise.

### /moderate
Returns a collection of content moderation tags. If a tag is "true" then the given text has been classified as that category.
Use /moderate after a /filter-check to elaborate on the type of hateful or harmful content detected.

Example: "Harrassment" : true means the given text was classified as harassment activity.

### /fact-check
Checks if the given text is misinformation. Returns a number from 1-10, the lower the number the more likely it is to be misinformation.

### /offensiveness
Checks if the given text contains offensive content. Returns a number from 1-10, the higher the number the more likely it is to be offensive speech.

### /hateful-image
This endpoint must be called with a POST, containing the field "image" which holds base64 image data to be classified.

Checks if the given image conatins hateful content. Returns True if hateful content was found, False otherwise.

## Running the API
1. Create your virtual environment. 
2. Install all packages in requirements.txt.
3. Create a .env file in the backend. It should have two keys: OPEN_API_KEY with a Open AI API key, and API_TOKEN with a hugging face key.
4. With your terminal sitting in ai-moderation-apis/backend run "flask --app main run --debug". 

It should now be running on http://127.0.0.1:5000.

## Models Used
### Text Processing
[Open AI Moderation API](https://platform.openai.com/docs/guides/moderation)

[Open AI ChatGPT 3.5-Turbo](https://openai.com/chatgpt)

### Image Processing
[Open AI Zero-Shot Image Classification](https://huggingface.co/openai/clip-vit-large-patch14)

[Laion-2B Zero-Shot Image Classification by Romain Beaumont](https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K)

[Pickscore Zero-Shot Image Classification by Yuval Kirstain, Adam Polyak, Uriel Singer, Shahbuland Matiana, Joe Penna and Omer Levy](https://huggingface.co/yuvalkirstain/PickScore_v1)
