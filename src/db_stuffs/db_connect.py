import ibm_db 
import os
import uuid 
import data

password = "XIho3BxFB7Z4u2Hj"
username = "nlz47787"
database = "bludb"
hostname = '8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud'
#path =  'D:\Projectlads\Face-Mask-Detection\src\db_stuffs\certificate.crt'
path = "/home/rupam/Face-Mask-Detection/src/db_stuffs/certificate.crt"
port = 30120

uri =f"DATABASE={database};HOSTNAME={hostname};PORT={port};SECURITY=SSL;SSLServerCertificate={path};UID={username};PWD={password}" 

try:
    conn1 = ibm_db.connect(uri , '' , '')
    print("[1]---  Success ----")

    import ibm_db_dbi 
    conn2 = ibm_db_dbi.Connection(conn1)
    print("[2]--- Success ---")

    t = conn2.tables('NLZ47787' , '%')
    print("---- TABLES ---- ")
    for table in t:
        print(table['TABLE_NAME'])
    
    data.read_path(conn1, conn2)
    
    print("----------------")
    ibm_db.close(conn1)
    print("Connection closed")


    
except Exception as e:
    import sys    
    print(e)
    sys.exit()



