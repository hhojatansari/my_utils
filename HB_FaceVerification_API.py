import requests


API_ENDPOINT = "http://api.hibrainy.com/api/v1/Face/FaceVerification"
API_KEY = "Your Api Key"

image1 = '1.jpg'    # path to image
image2 = '2.jpg'    # path to image

files = {'Photo1': (image1, open(image1, 'rb'), "multipart/form-data"),
         'Photo2': (image2, open(image2, 'rb'), "multipart/form-data")}
header = {'API-Key': API_KEY}

response = requests.post(API_ENDPOINT, files=files, headers=header)

print('ResultMessage:', response.json()['ResultMessage'])
print('SimilarPercent', response.json()['SimilarPercent'])