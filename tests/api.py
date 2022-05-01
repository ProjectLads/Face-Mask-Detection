from PIL import Image as image 
import base64
import requests 
import os 
import matplotlib.pyplot as plt
import numpy as np
import cv2
from requests.models import Response 

def send_sms(phone_number, message):
    url = f"https://www.fast2sms.com/dev/bulkV2?authorization=XqTFcAC4MktpQsSyKEnvPeOwjB51rhdR78YNDWVHg6bzIuo9fJNhi0OcLFJIV3sndbty42mEZ5XrHfpg&route=v3&sender_id=TXTIND&message={message}&language=english&flash=0&numbers={phone_number}"
    resp = requests.get(url)
    try:
        if resp.status_code != 200:
            print(resp.content)
            raise Exception("Something must have went wrong with SMS Service trial. Please Check")
    except Exception as e :
        pass

def face_match(image1 , image2 , apikey):
    #PATH1 = os.getcwd() + "/tmp/image1.jpeg"
    #PATH2 = os.getcwd() + "/tmp/image2.jpeg"
    PATH1 = "/home/rupam/Face-Mask-Detection/src/MainApp/tmp/image1.jpeg"
    PATH2 = "/home/rupam/Face-Mask-Detection/src/MainApp/tmp/image2.jpeg"


    image.fromarray(image1.astype(np.uint8)).save(PATH1 , quality = 100)
    image.fromarray(image2.astype(np.uint8)).save(PATH2 , quality = 100)

    img1 = open(PATH1 , 'rb').read()
    img2 = open(PATH2 , 'rb').read()

    image3 = cv2.imread(PATH2)
    
    plt.imshow(image3)
    plt.show()

    input(' > NEXT -> ')
    
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
        return False







