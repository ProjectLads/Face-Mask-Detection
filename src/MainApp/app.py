import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import ibm_db
import json 
import base64
import requests
from PIL import Image as image




image_to_text  = lambda image: json.dumps(image.tolist())
text_to_image  = lambda text:  np.array(json.loads(text))



def face_match(image1 , image2 , apikey):
    #PATH1 = os.getcwd() + "/tmp/image1.jpeg"
    #PATH2 = os.getcwd() + "/tmp/image2.jpeg"
    PATH1 = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/tmp/image1.jpeg"
    PATH2 = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/tmp/image2.jpeg"


    image.fromarray(image1.astype(np.uint8)).save(PATH1 , quality = 100)
    image.fromarray(image2.astype(np.uint8)).save(PATH2 , quality = 100)

    img1 = open(PATH1 , 'rb').read()
    img2 = open(PATH2 , 'rb').read()

    #image3 = cv2.imread(PATH2)
    
    #plt.imshow(image3)
    #plt.show()

    #input(' > NEXT -> ')
    
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
        #return False
        print(resp.content)
        return "poor quality"


def send_sms(phone_number, message):
    url = f"https://www.fast2sms.com/dev/bulkV2?authorization=XqTFcAC4MktpQsSyKEnvPeOwjB51rhdR78YNDWVHg6bzIuo9fJNhi0OcLFJIV3sndbty42mEZ5XrHfpg&route=v3&sender_id=TXTIND&message={message}&language=english&flash=0&numbers={phone_number}"
    resp = requests.get(url)
    try:
        if resp.status_code != 200:
            print(resp.content)
            raise Exception("Something must have went wrong with SMS Service trial. Please Check")
    except Exception as e :
        pass

def search(test_image, conn1):
    query  = '''Select * from USER_IMAGE'''
    statement = ibm_db.prepare(conn1 , query)
    ibm_db.execute(statement)
    result_set = ibm_db.fetch_tuple(statement)
    
    while result_set:
        query  = '''Select * from USER_INFO where UID=?'''
        user_id = result_set[3] 
        img_arr1 = text_to_image(result_set[1])
        img_arr2 = text_to_image(result_set[2])
        apikey = "I39243ua8sbTpjaN2632"
        match1 = face_match(test_image , img_arr1, apikey)
        match2 = face_match(test_image , img_arr2 ,apikey)
        #if face_match(test_image , img_arr1, apikey) or face_match(test_image , img_arr2 ,apikey):
        if match1 == "poor quality" or match2 == "poor quality":
            return "poor quality"
        if match1 or match2:
            statement1 = ibm_db.prepare(conn1 , query)
            ibm_db.execute(statement1, (user_id, ))
            result = ibm_db.fetch_tuple(statement1)
        
            #print(result[0], result[1], result[2], result[3], result[4], result[5])
            #phone_number = result[3]
            #found = True
            #break
            return result[1]
        
        result_set = ibm_db.fetch_tuple(statement)
    
    return "Face not found"
    #if found:
        #print("image found")
        #message = '''You haven't worn a mask. Please wear a mask for everyone's safety! Join us: https://meet.google.com/wrh-kdfz-bmf 
#With regards,
#ProjectLads'''
        #send_sms(phone_number, message)
    #else:
    #    print("image not found")


def mainloop(conn , model):
    cap = cv2.VideoCapture(0)
    print("started")
    if not cap.isOpened():
        raise IOError("Can't open webcam")



    while True:
        ret, frame = cap.read()
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        Image.fromarray(frame.astype(np.uint8)).save("C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/tmp/frame.jpeg" , quality = 100)

        frame = cv2.imread("C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/tmp/frame.jpeg")

        os.remove("C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/tmp/frame.jpeg")
        #cv2.imshow('Face Mask Detector', frame)        
        boxes = faceCascade.detectMultiScale(frame, 1.1, 4)
        for x, y, w, h in boxes:
            
            roi_color = frame[y:y+h, x:x+w]
            faces = faceCascade.detectMultiScale(roi_color)
            message = ""
            if len(faces) > 0:
                name = search(roi_color, conn)
                
                if name == -1:
                    message = "Face not found"
                else:
                    message = name
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, message, (x,y), font, 1, (255, 0, 0), 2)



        cv2.imshow('Face Mask Detector', frame)
    

        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()
