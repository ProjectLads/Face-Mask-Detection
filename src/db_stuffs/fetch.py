import ibm_db
import convert
import matplotlib.pyplot as plt

'''DATA_DIR = "D:\Projectlads\Face-Mask-Detection\src\db_stuffs\data.csv"
info = []
with open(DATA_DIR) as data:
    for row in data:
        info.append(row.split(',')[1:6])
    info = info[1:]
    print(info)'''
    
query  = '''Select * from USER_IMAGE'''
password = "XIho3BxFB7Z4u2Hj"
username = "nlz47787"
database = "bludb"
hostname = '8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud'
path =  'D:\Projectlads\Face-Mask-Detection\src\db_stuffs\certificate.crt'
port = 30120

uri =f"DATABASE={database};HOSTNAME={hostname};PORT={port};SECURITY=SSL;SSLServerCertificate={path};UID={username};PWD={password}" 


conn1 = ibm_db.connect(uri , '' , '')
    
#parameters = ((text1 , text2, user_id) , )
#print(len(text1), len(text2))
    
statement = ibm_db.prepare(conn1 , query)
ibm_db.execute(statement)
result_set = ibm_db.fetch_tuple(statement)
while result_set:
    query  = '''Select * from USER_INFO where UID=?'''
    user_id = result_set[3] 
    
    statement1 = ibm_db.prepare(conn1 , query)
    ibm_db.execute(statement1, (user_id, ))
    result = ibm_db.fetch_tuple(statement1)
    print(result[0], result[1], result[2], result[3], result[4], result[5])
    img_arr1 = convert.text_to_image(result_set[1])
    img_arr2 = convert.text_to_image(result_set[2])
    plt.imshow(img_arr1)
    plt.show()
    input()
    plt.imshow(img_arr2)
    plt.show()
    input()
    #print(result_set[3])
    result_set = ibm_db.fetch_tuple(statement)
    