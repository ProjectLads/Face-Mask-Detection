import requests

with open('mask.jpg' , 'rb') as image:
    img_file = {'image' : image}
    result = requests.post('http://127.0.0.1:5000/' , files = img_file)

print(result.text)
print('Test Successful')

