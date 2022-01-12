import cv2, convert, uuid, ibm_db, os 
import matplotlib.pyplot as plt
DATA_DIR = "/home/rupam/Face-Mask-Detection/src/db_stuffs/data.csv"
IMAGE_MASK_DIR = "/home/rupam/Face-Mask-Detection/src/db_stuffs/images/mask"

IMAGE_UNMASK_DIR = "/home/rupam/Face-Mask-Detection/src/db_stuffs/images/withoutMask"

info =[]
image = []

def insert_into_image_table(text1, text2, user_id, conn1):
    query  = '''INSERT INTO 
    USER_IMAGE(MASK_IMAGE , UNMASK_IMAGE , USER_ID) 
    VALUES(? , ? , ?)'''
    
    parameters = ((text1 , text2, user_id) , )
    
    
    statement = ibm_db.prepare(conn1 , query)
    ibm_db.execute_many(statement , parameters)


def insert_into_user_table(user_id, name, country_code, phone_number, email_id, address, conn1):
    
    
    query  = '''Insert into 
    user_info(UID, Name,Country_code,Phone_number,Email_id,Address) 
    values(?, ?, ?, ?, ?, ?);'''
    
    parameters = ((user_id, name, country_code, phone_number, email_id, address) , )
    
    statement = ibm_db.prepare(conn1 , query)
    ibm_db.execute_many(statement , parameters)

    

def detect_face(frame):
    
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    boxes = faceCascade.detectMultiScale(frame, 1.1, 4)
    for x, y, w, h in boxes:
        roi_color = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
        faces = faceCascade.detectMultiScale(roi_color)
        if len(faces) > 0:
            return roi_color

    print("No face")
    return frame

            
def read_path(conn1, conn2):
    DATA_DIR = "/home/rupam/Face-Mask-Detection/tests/data.csv"
    IMAGE_MASK_DIR = "/home/rupam/Face-Mask-Detection/tests/images/mask"

    IMAGE_UNMASK_DIR = "/home/rupam/Face-Mask-Detection/tests/images/withoutMask"
    info =[]
    image = []
    


    with open(DATA_DIR) as data:
        for row in data:
            info.append(row.split(',')[1:6])
        info = info[1:]
        for row in info:
            name, country_code, phone_number, email_id, address = row[0], row[1], row[2], row[3], row[4]
            #print(name, country_code, phone_number, email_id, address)
            img_mask = cv2.imread(IMAGE_MASK_DIR + '/' + row[0] + '.jpeg')
            img_unmask = cv2.imread(IMAGE_UNMASK_DIR + '/' + row[0] + '.jpeg')
            img_mask = cv2.resize(detect_face(img_mask) , (500 , 500))
            img_unmask = cv2.resize(detect_face(img_unmask) , (500 , 500))
            plt.imshow(img_mask)
            plt.show()
            input()

            plt.imshow(img_unmask)
            plt.show()

            input()
            #print(img_mask.shape, img_unmask.shape)
            text1 = convert.image_to_text(img_mask) if (img_mask is not None) else None
            text2 = convert.image_to_text(img_unmask) if (img_unmask is not None) else None
            user_id_uuid =str(uuid.uuid1())
            print("Hi1")
            insert_into_user_table(user_id_uuid, name, country_code, phone_number, email_id, address, conn1)
            print("Hi2")
            insert_into_image_table(text1, text2, user_id_uuid, conn1)
            print("Hi3")






