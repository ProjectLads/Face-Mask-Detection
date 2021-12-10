import ibm_db 
import os 

password = os.environ["password"]
username = os.environ["username"]
database = os.environ["database"]
hostname = os.environ["hostname"]
path =  os.environ["ssl_certificate"]
port = os.environ["port"]

uri =f"DATABASE={database};HOSTNAME={hostname};PORT={port};SECURITY=SSL;SSLServerCertificate={path};UID={username};PWD={password}" 

def insert_into_image_table():
    import convert , cv2 
    image = cv2.imread('mask.jpg')
    text = convert.image_to_text(image)
    
    query  = 'INSERT INTO USER_IMAGE(MASK_IMAGE , UNMASK_IMAGE , USER_ID) VALUES(? , ? , ?)'
    parameters = ((text , None , 1) , )
    
    statement = ibm_db.prepare(conn1 , query)
    ibm_db.execute_many(statement , parameters)


def insert_into_user_table():
    
    query  = 'INSERT INTO USER_IMAGE(MASK_IMAGE , UNMASK_IMAGE , USER_ID) VALUES(? , ? , ?)'
    parameters = ((text , None , 1) , )
    
    statement = ibm_db.prepare(conn1 , query)
    ibm_db.execute_many(statement , parameters)






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

    print("----------------")
    ibm_db.close(conn1)
    print("Connection closed")
    
except Exception as e:
    import sys    
    print(e)
    sys.exit()


