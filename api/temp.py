import requests
import json

QUERY_URL = "https://api.openai.com/v1/images/generations"


def generate_image(prompt, model, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "prompt": prompt,
        "num_images": 1,
        "size": "1024x1024",
        "response_format": "url"
    }
    resp = requests.post(QUERY_URL, headers=headers, data=json.dumps(data))
    if resp.status_code != 200:
        raise ValueError("Failed to generate image")
    response_text = json.loads(resp.text)
    return response_text['data'][0]['url']


response = requests.get("https://api.dicebear.com/5.x/adventurer/svg")
print(response.content)

# # DALL-E API endpoint
# url = "https://api.openai.com/v1/images/generations"

# # API key for authentication
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Bearer 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"
# }

# # Request payload with the text prompt
# data = {
#     "model": "image-alpha-001",
#     "prompt": "generate a picture of a dog",
#     "num_images": 1,
#     "size": "1024x1024",
#     "response_format": "url"
# }

# # Make the API request
# response = requests.post(url, headers=headers, data=json.dumps(data))

# # Check if the request was successful
# if response.status_code == 200:
#     # Get the image URL from the response
#     image_url = response.json()["data"][0]["url"]

#     # Download the image and save it to a file
#     image_response = requests.get(image_url)
#     with open("dog_image.jpg", "wb") as f:
#         f.write(image_response.content)

# else:
#     # Handle the error
#     print("Failed to generate image:", response.text)
