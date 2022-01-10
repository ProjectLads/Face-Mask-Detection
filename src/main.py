import ibm_db 
import os 

import tensorflow as tf
from app import mainloop 

password = "XIho3BxFB7Z4u2Hj"
username = "nlz47787"
database = "bludb"
hostname = '8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud'
#path =  'D:\Projectlads\Face-Mask-Detection\src\db_stuffs\certificate.crt'
path = "/home/rupam/Face-Mask-Detection/src/db_stuffs/certificate.crt"
port = 30120

uri =f"DATABASE={database};HOSTNAME={hostname};PORT={port};SECURITY=SSL;SSLServerCertificate={path};UID={username};PWD={password}" 


if __name__ == '__main__':
    
    conn1 = ibm_db.connect(uri , '' , '')

    import ibm_db_dbi 
    conn2 = ibm_db_dbi.Connection(conn1)

    print("DB CONNECTED")

    model = tf.keras.models.load_model(os.getcwd() + "/models/model_2.h5")




    mainloop(conn1 , model)





    ibm_db.close(conn1)
    print("Connection closed")


    
    



