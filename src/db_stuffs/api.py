import cv2
import matplotlib.pyplot as plt
import data, base64
import numpy as np
import requests 

#my_url = https://faceapi.mxface.ai/api/face/verify
my_url_token = 'I39243ua8sbTpjaN2632'



img1 = cv2.imread("C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/image1.jpeg")
img2 = cv2.imread("C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/image2.jpg")
#print(img1)
#print(img2)


img1 = data.detect_face(img1)
img2 = data.detect_face(img2)

img1 = cv2.resize(img1 ,  (31 , 31))
img2 = cv2.resize(img2 ,  (31 , 31))

img1string = base64.b64encode(np.ascontiguousarray(img1))
img2string = base64.b64encode(np.ascontiguousarray(img2))

#print(img1string)

headers = { 
"Content-Type" : "application/json",

"Subscriptionkey" : "I39243ua8sbTpjaN2632" ,
"encoded_image1" : img1string ,
"encoded_image2" : img2string
}

#data = {
#"encoded_image1" : img1string ,
#"encoded_image2" : img2string
#}

plt.imshow(img1)
plt.show()
input()
plt.imshow(img2)
plt.show()
url = f'https://faceapi.mxface.ai/api/face/verify'
print(len(url))

#?encoded_image1={img1string}&encoded_image2={img2string}

#resp = requests.post(url , headers=headers)
#print(resp.status_code)
#print(resp.reason)
print(headers)
