import requests

with open('unmask.jpg' , 'rb') as image:
    img_file = {'image' : image}
    result = requests.post('https://maskpredictor.herokuapp.com/predict' , files = img_file)

print(result.text)
print('Test Successful')

