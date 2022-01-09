from PIL import Image as image 
 
import base64
import requests 
import os 

def face_match(image1 , image2 , apikey):
    PATH1 = os.getcwd() + "/tmp/image1.jpeg"
    PATH2 = os.getcwd() + "/tmp/image2.jpeg"

    image.fromarray(image1).save(PATH1)
    image.fromarray(image2).save(PATH2)

    
    img1 = open(PATH1 , 'rb').read()
    img2 = open(PATH2 , 'rb').read()

    
    img1string = base64.b64encode(img1).decode("utf-8")
    img2string = base64.b64encode(img2).decode("utf-8")

    os.remove(PATH1)
    os.remove(PATH2)

    headers = { 
        "Content-Type" : "application/json",

        "Subscriptionkey" : apikey ,

        }
    data1 = {}

    data1["encoded_image1"]  =  img1string
    data1["encoded_image2"] =   img2string

    url = f'https://faceapi.mxface.ai/api/face/verify'


    resp = requests.post(url , headers=headers , json=data1)
    if resp.status_code == 200 : 
        return True if (resp.json()["confidence"] > 0.50) else False
    else:
        print(resp.reason)









apikey = "I39243ua8sbTpjaN2632"

print(face_match(img1 , img2 , apikey))


