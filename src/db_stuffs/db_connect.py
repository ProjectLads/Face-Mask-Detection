import ibm_db 
import os
import uuid 

password = "XIho3BxFB7Z4u2Hj"
username = "nlz47787"
database = "bludb"
hostname = '8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud'
path =  'D:\Projectlads\Face-Mask-Detection\src\db_stuffs\certificate.crt'
port = 30120

uri =f"DATABASE={database};HOSTNAME={hostname};PORT={port};SECURITY=SSL;SSLServerCertificate={path};UID={username};PWD={password}" 

def insert_into_image_table(mask_image, unmask_image, user_id):
    import convert , cv2 
    image_mask = cv2.imread(mask_image) if (mask_image is not None) else None
    text1 = convert.image_to_text(image_mask)
    
    image_unmask = cv2.imread(unmask_image) if (unmask_image is not None) else None
    text2 = convert.image_to_text(image_unmask) 
    
    query  = '''INSERT INTO 
    USER_IMAGE(MASK_IMAGE , UNMASK_IMAGE , USER_ID) 
    VALUES(? , ? , ?)'''
    
    parameters = ((text1 , text2, user_id) , )
    
    statement = ibm_db.prepare(conn1 , query)
    ibm_db_user_table_executeibm_db.execute_many(statement , parameters)


def insert_into_user_table(user_id, name, country_code, phone_number, email_id, address):
    
    
    query  = '''Insert into 
    user_info(UID, Name,Country_code,Phone_number,Email_id,Address) 
    values(?, ?, ?, ?, ?, ?);'''
    
    parameters = ((user_id, name, country_code, phone_number, email_id, address) , )
    
    statement = ibm_db.prepare(conn1 , query)
    ibm_db.execute_many(statement , parameters)
    print(user_id,'Hello')





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
    
    user_id_uuid =str(uuid.uuid1())
    insert_into_user_table(user_id_uuid, 'a', '+91', 1234567895, 'b', 'c')
    insert_into_image_table('D:\Projectlads\Face-Mask-Detection\src\db_stuffs\mask.jpg', None, user_id_uuid)

    print("----------------")
    ibm_db.close(conn1)
    print("Connection closed")


    
except Exception as e:
    import sys    
    print(e)
    sys.exit()



