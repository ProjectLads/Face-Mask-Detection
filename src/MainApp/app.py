import cv2
from PIL import Image
import numpy as np
import os
import ibm_db
import matplotlib.pyplot as plt
import cv2
import face_recognition
import json 


image_to_text  = lambda image: json.dumps(image.tolist())
text_to_image  = lambda text:  np.array(json.loads(text))

class Application:

    def __init__(self):
        self.config = dict()

    def search(self , conn, test_image):
        query  = '''Select * from USER_IMAGE'''
        statement = ibm_db.prepare(conn , query)
        ibm_db.execute(statement)
        result_set = ibm_db.fetch_tuple(statement)
        while result_set:
            query  = '''Select * from USER_INFO where UID=?'''
            user_id = result_set[3] 
            img_arr1 = text_to_image(result_set[1])
            img_arr2 = text_to_image(result_set[2])
                   
            match1 = self.face_match(test_image , img_arr1)
            match2 = self.face_match(test_image , img_arr2)
                                  
            if match1 or match2:
                statement1 = ibm_db.prepare(conn , query)
                ibm_db.execute(statement1, (user_id, ))
                result = ibm_db.fetch_tuple(statement1)
            
                return result[1]
            
            result_set = ibm_db.fetch_tuple(statement)
        
        return "Face not found"

    def face_match(self , image1 , image2):
        
        PATH1 = self.config["TEMP"] + "image1.jpeg"
        PATH2 = self.config["TEMP"] + "image2.jpeg"


        Image.fromarray(image1.astype(np.uint8)).save(PATH1 , quality = 100)
        Image.fromarray(image2.astype(np.uint8)).save(PATH2 , quality = 100)

        
        image1 = face_recognition.load_image_file(PATH1)
        image2 = face_recognition.load_image_file(PATH2)
        
        w1 = image1.shape[0]
        h1 = image1.shape[1]
        w2 =  image2.shape[0]
        h2 =  image2.shape[1]

        encoding_1 = face_recognition.face_encodings(image1, known_face_locations = [(0, w1, h1, 0)])
        encoding_2 = face_recognition.face_encodings(image2, known_face_locations = [(0, w2, h2, 0)])
        
        os.remove(PATH1)
        os.remove(PATH2)


        results = face_recognition.compare_faces([encoding_1[0]], encoding_2[0])
        
        
        return results[0]

        
       
    def mainloop(self , conn):
        cap = cv2.VideoCapture(0)
        print("started")
        if not cap.isOpened():
            raise IOError("Can't open webcam")


        cap.set(11, 1.0)
        cap.set(6, 70.0)
        cap.set(7, 30.0)
        cap.set(1, 1024)
        cap.set(2, 1024)

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        while True:
            ret, frame = cap.read()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            faces = faceCascade.detectMultiScale(gray, 1.1, 4)
            bottom_message = "Project Lads"
            bottom_x , bottom_y = (frame.shape[0] , frame.shape[1])
            for x, y, w, h in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
                facess = faceCascade.detectMultiScale(roi_gray)
                if len(facess) == 0:
                    print("Face not detected")
                    message = "Face not detected"
                    
                else:
                    print("Face Detection Success")
                    message = self.search(conn, roi_color)
                    print(message)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, message, (x, y), font, 1, (0, 0, 255))
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
        
            
            cv2.imshow('Mask-Inspector', frame)
        

            if cv2.waitKey(1) == 13:
                break

        cap.release()
        cv2.destroyAllWindows()
            
    def run(self):
        
        username = self.config["USER"]
        password = self.config["PASSWORD"]

        database = self.config["DATABASE"]

        hostname = self.config["HOST"]

        port = self.config["PORT"]

        path = self.config["CERTIFICATE"]

    

        uri =f"DATABASE={database};HOSTNAME={hostname};PORT={port};SECURITY=SSL;SSLServerCertificate={path};UID={username};PWD={password}"      
        conn = ibm_db.connect(uri , '' , '')

        self.mainloop(conn)

        ibm_db.close(conn)

        print("Connection closed")


