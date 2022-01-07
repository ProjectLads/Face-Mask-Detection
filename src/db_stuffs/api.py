import cv2
import matplotlib.pyplot as plt
import data, base64
import numpy as np


#my_url = https://faceapi.mxface.ai/api/face/verify
my_url_token = 'I39243ua8sbTpjaN2632'
"""
headers = { 
"Content-Type" : "application/json"

"Subscriptionkey" : "I39243ua8sbTpjaN2632" 
}
"""
img1 = cv2.imread("C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/image1.jpeg")
img2 = cv2.imread("C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/image2.jpg")
#print(img1)
#print(img2)


img1 = data.detect_face(img1)
img2 = data.detect_face(img2)

img1string = base64.b64encode(np.ascontiguousarray(img1))
img2string = base64.b64encode(np.ascontiguousarray(img2))

print(img1string)

plt.imshow(img1)
plt.show()
input()
plt.imshow(img2)
plt.show()
url = f'https://faceapi.mxface.ai/api/face/verify?encoded_image1={img1}&encoded_image2={img2}'
