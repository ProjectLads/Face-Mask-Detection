from app import Application
import cv2 
import requests
import matplotlib.pyplot as plt
import json

def detect_face(frame):
    
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    boxes = faceCascade.detectMultiScale(frame, 1.1, 4)
    
    
    
    for x, y, w, h in boxes:
        
        roi_color = frame[y:y+h, x:x+w]
        faces = faceCascade.detectMultiScale(frame, 1.1, 4)

        if len(faces) > 0:
            
            _ , img = cv2.imencode('.jpg' , roi_color)
            resp = requests.post("https://maskpredictor.herokuapp.com/predict" , data = img.tobytes())
            d = json.loads(resp.text)
            message , color = ("No Mask" , (255 , 0 , 0)) if d["prediction"] == 0 else ("Mask" , (0 , 255 , 0))
            
            font = cv2.FONT_HERSHEY_SIMPLEX

            cv2.rectangle(frame, (x,y), (x+w, y+h), color , 2)

            

            cv2.putText(frame , message , (x ,y) , font , 1 ,color)
            



    return frame

    
            

            

import sys

image = cv2.imread(sys.argv[1])

frame = detect_face(image)

plt.imshow(frame)
plt.show()
