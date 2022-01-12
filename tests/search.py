import ibm_db
import convert
import matplotlib.pyplot as plt
import cv2
from data import detect_face
from api import face_match, send_sms
import tensorflow as tf
import numpy as np
from testing_main import decode_pred

query  = '''Select * from USER_IMAGE'''
password = "XIho3BxFB7Z4u2Hj"
username = "nlz47787"
database = "bludb"
hostname = '8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud'
path =  'C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/tests/certificate.crt'

#path = '/home/rupam/Face-Mask-Detection/src/db_stuffs/certificate.crt'
port = 30120
uri =f"DATABASE={database};HOSTNAME={hostname};PORT={port};SECURITY=SSL;SSLServerCertificate={path};UID={username};PWD={password}" 


conn1 = ibm_db.connect(uri , '' , '')

statement = ibm_db.prepare(conn1 , query)

ibm_db.execute(statement)
result_set = ibm_db.fetch_tuple(statement)

#PATH = "/home/rupam/Face-Mask-Detection/src/db_stuffs/image1.jpeg"
PATH = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/tests/RC.jpeg"
test_image = cv2.imread(PATH)
test_image = cv2.resize(detect_face(test_image) , (300 , 300))

test_model = tf.keras.models.load_model("C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/webapp/src/models/model_2.h5")

final_image = cv2.resize(test_image, (224, 224))
final_image = final_image/255.0
#plt.imshow(final_image)
#plt.show()
final_image = np.expand_dims(final_image, axis = 0)
#final_image = final_image/255.0


prediction = test_model.predict(final_image)
prediction = decode_pred(prediction[0])

if prediction == 0:
    print("No mask")
else:
    print("Mask")

if prediction == 0:
    while result_set:
        query  = '''Select * from USER_INFO where UID=?'''
        user_id = result_set[3] 
        img_arr1 = convert.text_to_image(result_set[1])
        img_arr2 = convert.text_to_image(result_set[2])
        apikey = "I39243ua8sbTpjaN2632"
    
    
        if face_match(test_image , img_arr1, apikey) or face_match(test_image , img_arr2 ,apikey):
            statement1 = ibm_db.prepare(conn1 , query)
            ibm_db.execute(statement1, (user_id, ))
            result = ibm_db.fetch_tuple(statement1)
        
            #print(result[0], result[1], result[2], result[3], result[4], result[5])
            phone_number = result[3]
            found = True
            break

        

        result_set = ibm_db.fetch_tuple(statement)
    

    if found:
        print("image found")
        message = '''You haven't worn a mask. Please wear a mask for everyone's safety! Join us: https://meet.google.com/wrh-kdfz-bmf 
With regards,
ProjectLads'''
        send_sms(phone_number, message)
    else:
        print("image not found")

ibm_db.close(conn1)