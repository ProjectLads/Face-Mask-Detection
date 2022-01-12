import cv2
from PIL import Image
import numpy as np
import os
import base64
import ibm_db
import numpy as np ,cv2
import json 
import requests
import matplotlib.pyplot as plt



image_to_text  = lambda image: json.dumps(image.tolist())
text_to_image  = lambda text:  np.array(json.loads(text))


def search(conn, test_image):
    query  = '''Select * from USER_IMAGE'''
    statement = ibm_db.prepare(conn , query)
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
        if match1 == "Poor quality" or match2 == "Poor quality":
            return "Poor quality"
        
        if match1 or match2:
            statement1 = ibm_db.prepare(conn , query)
            ibm_db.execute(statement1, (user_id, ))
            result = ibm_db.fetch_tuple(statement1)
        
            #print(result[0], result[1], result[2], result[3], result[4], result[5])
            #phone_number = result[3]
            #found = True
            #break
            return result[1]
        
        result_set = ibm_db.fetch_tuple(statement)
    
    return "Face not found"

        #result_set = ibm_db.fetch_tuple(statement)

def face_match(image1 , image2 , apikey):
    #PATH1 = os.getcwd() + "/tmp/image1.jpeg"
    #PATH2 = os.getcwd() + "/tmp/image2.jpeg"
    PATH1 = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/tmp/image1.jpeg"
    PATH2 = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/db_stuffs/tmp/image2.jpeg"


    Image.fromarray(image1.astype(np.uint8)).save(PATH1 , quality = 100)
    Image.fromarray(image2.astype(np.uint8)).save(PATH2 , quality = 100)

    img1 = open(PATH1 , 'rb').read()
    img2 = open(PATH2 , 'rb').read()

    image3 = cv2.imread(PATH1)
    image4 = cv2.imread(PATH2)

    plt.imshow(image3)
    plt.show()

    input(' > NEXT -> ')

    plt.imshow(image4)
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
        return "Poor quality"




def main(conn):
    cap = cv2.VideoCapture(0)
    print("started")
    if not cap.isOpened():
        raise IOError("Can't open webcam")
    ret, frame = cap.read()
    cap.set(11, 1.0)
    cap.set(6, 70.0)
    cap.set(7, 30.0)
    cap.set(1, 1024)
    cap.set(2, 1024)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    #Image.fromarray(frame.astype(np.uint8)).save(os.getcwd() + "/db_stuffs/tmp/frame.jpeg" , quality = 100)

    #frame = cv2.imread(os.getcwd() + "/db_stuffs/tmp/frame.jpeg")

    #os.remove(os.getcwd() + "/db_stuffs/tmp/frame.jpeg")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #
    faces = faceCascade.detectMultiScale(gray, 1.1, 4)
    for x, y, w, h in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
        facess = faceCascade.detectMultiScale(roi_gray)
        if len(facess) == 0:
            print("Face not detected")
        else:
            #for (ex, ey, ew, eh) in facess:
            #face_roi = roi_color[ey: ey+eh, ex: ex+ew]
            print("Face Detection Success")
    
    #boxes = faceCascade.detectMultiScale(frame, 1.1, 4)
    #for x, y, w, h in boxes:
        #roi_color = frame[y:y+h, x:x+w]
        #faces = faceCascade.detectMultiScale(roi_color)
        #if len(faces) > 0:
        #    message = search(conn, roi_color)
        #    font = cv2.FONT_HERSHEY_SIMPLEX
        #    cv2.putText(frame, message, (x, y), font, 1, (255, 0, 0))
        #else:
        #    message = "Face not detected"
        #    font = cv2.FONT_HERSHEY_SIMPLEX
        #    cv2.putText(frame, message, (x, y), font, 1, (0, 0, 255))
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
        plt.imshow(frame)
        plt.show()
        input()
    #cv2.imshow('Face Mask Detector', frame)
    #plt.imshow(frame)
    #plt.show()
    #input()

    cap.release()
    cv2.destroyAllWindows()


main("hello")
