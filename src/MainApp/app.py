import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def search(image):
    pass


def mainloop(conn , model):
    cap = cv2.VideoCapture(0)
    print("started")
    if not cap.isOpened():
        raise IOError("Can't open webcam")



    while True:
        ret, frame = cap.read()
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        Image.fromarray(frame.astype(np.uint8)).save(os.getcwd() + "/db_stuffs/tmp/frame.jpeg" , quality = 100)

        frame = cv2.imread(os.getcwd() + "/db_stuffs/tmp/frame.jpeg")

        os.remove(os.getcwd() + "/db_stuffs/tmp/frame.jpeg")
                
        boxes = faceCascade.detectMultiScale(frame, 1.1, 4)
        for x, y, w, h in boxes:
            
            roi_color = frame[y:y+h, x:x+w]
            faces = faceCascade.detectMultiScale(roi_color)
            if len(faces) > 0:
                pass

                

    

        cv2.imshow('Face Mask Detector', frame)
    

        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()
        
