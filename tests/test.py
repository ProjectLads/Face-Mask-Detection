import requests
import cv2 

img = cv2.imread('unmask.jpg')

_ , img = cv2.imencode('.jpeg' , img)

model_url = "http://192.168.29.231:5000/predict"
result = requests.post(model_url , data = img.tobytes())

print(result.text)
print('Test Successful')

