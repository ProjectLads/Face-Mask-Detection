import cv2
import tensorflow as tf 
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 

path = 'haarcascade_frontalface_default.xml'

test_model = tf.keras.models.load_model(os.getcwd() + '/models/model_2.h5')

def decode_pred(prob):
    if prob >= 0.5:
        return 1
    else:
        return 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Can't open webcam")

final_images = []

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

            final_image = cv2.resize(roi_color, (224, 224))
            
            final_image = np.expand_dims(final_image, axis = 0)
            final_image = final_image/255.0

            prediction = test_model.predict(final_image)
            prediction = decode_pred(prediction[0])

            final_images.append((roi_color , prediction))


            if(prediction == 1):
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)
        else:
            final_images.append((roi_color , 'Face not detected'))


            cv2.rectangle(frame, (x,y), (x+w, y+h), (255 , 0 ,  0), 2)


    

    cv2.imshow('Face Mask Detector', frame)
    

    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()

input('CHECK ANALYTICS : ')

for image in final_images:

    plt.imshow(image[0])
    plt.show()
    print('Prediction :' , image[1])
    input()

