import requests


API_ENDPOINT = "http://api.hibrainy.com/api/v1/Face/FaceAllFeatures"
API_KEY = "Your Api Key"

image = '1.jpg'    # path to image

files = {'Photo': (image, open(image, 'rb'), "multipart/form-data")}
header = {'API-Key': API_KEY}

response = requests.post(API_ENDPOINT, files=files, headers=header)

for i in range(0, len(response.json())):
    print('Gender:', response.json()[i]['Gender'])
    print('Age:', response.json()[i]['Age'])
    print('FaceBox:', response.json()[i]['Rectangle'])
    # other Features